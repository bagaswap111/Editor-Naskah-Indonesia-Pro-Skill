import json
import os
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# No default on purpose. Flask signs session cookies with SECRET_KEY, so a value
# that is published in this repository lets anyone mint an `is_admin` cookie and
# walk straight into /admin without the password. Refuse to start instead.
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError(
        'SECRET_KEY is not set. Generate one with `openssl rand -hex 32` and put it '
        'in .env (see .env.example). The app will not start without it, because a '
        'guessable key allows forging admin session cookies.'
    )
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'evaluations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('ADMIN_COOKIE_SECURE', '1') == '1'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Caddy is the only thing in front of the app and compose binds the app to
# loopback, so trusting a single proxy hop is safe. Without this, Flask sees the
# proxy's address instead of the evaluator's and builds http:// URLs behind TLS.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

db = SQLAlchemy(app)
CORS(app)


class Evaluator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    consent_date = db.Column(db.DateTime, default=datetime.utcnow)
    consent_given = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    evaluations = db.relationship('Evaluation', backref='evaluator', lazy=True)


class Manuscript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(50), unique=True, nullable=False)
    style = db.Column(db.String(50), nullable=False)
    manuscript_type = db.Column(db.String(50), nullable=False)
    original_path = db.Column(db.String(200), nullable=False)
    outputs = db.relationship('Output', backref='manuscript', lazy=True)


class Output(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manuscript_id = db.Column(db.Integer, db.ForeignKey('manuscript.id'), nullable=False)
    system_type = db.Column(db.String(20), nullable=False)
    output_file = db.Column(db.String(200), nullable=False)


class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('evaluator.id'), nullable=False)
    manuscript_id = db.Column(db.Integer, db.ForeignKey('manuscript.id'), nullable=False)
    output_type = db.Column(db.String(20), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)

    score_kejelasan = db.Column(db.Integer)
    score_koherensi = db.Column(db.Integer)
    score_kedalaman = db.Column(db.Integer)
    score_akurasi = db.Column(db.Integer)
    score_gaya = db.Column(db.Integer)
    score_mekanik = db.Column(db.Integer)
    score_engagement = db.Column(db.Integer)

    comment_kejelasan = db.Column(db.Text)
    comment_koherensi = db.Column(db.Text)
    comment_kedalaman = db.Column(db.Text)
    comment_akurasi = db.Column(db.Text)
    comment_gaya = db.Column(db.Text)
    comment_mekanik = db.Column(db.Text)
    comment_engagement = db.Column(db.Text)

    is_draft = db.Column(db.Boolean, default=True)
    completed_at = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('evaluator_id', 'manuscript_id', 'output_type'),
    )


class GeneralComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('evaluator.id'), nullable=False)
    strengths = db.Column(db.Text)
    weaknesses = db.Column(db.Text)
    suggestions = db.Column(db.Text)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        name = request.form.get('name')
        consent_given = request.form.get('consent') == 'on'

        if name and consent_given:
            evaluator = Evaluator(name=name, consent_given=True)
            db.session.add(evaluator)
            db.session.commit()
            session['evaluator_id'] = evaluator.id
            return redirect(url_for('instructions'))

    return render_template('consent.html')


@app.route('/instructions')
def instructions():
    if 'evaluator_id' not in session:
        return redirect(url_for('consent'))
    return render_template('instructions.html')


def build_page_list():
    """Build list of available pages based on existing outputs."""
    manuscripts = Manuscript.query.order_by(Manuscript.id).all()
    pages = []
    page_num = 1
    
    for m in manuscripts:
        # Always add ENIP page
        enip_output = Output.query.filter_by(manuscript_id=m.id, system_type='enip').first()
        if enip_output:
            output_path = os.path.join(basedir, 'data', 'enip_outputs', enip_output.output_file)
            if os.path.exists(output_path):
                pages.append({
                    'page': page_num,
                    'manuscript': m,
                    'output_type': 'enip',
                    'label': f'{m.file_id} ENIP'
                })
                page_num += 1
        
        # Add B1 page only if output exists
        b1_output = Output.query.filter_by(manuscript_id=m.id, system_type='b1').first()
        if b1_output:
            output_path = os.path.join(basedir, 'data', 'b1_outputs', b1_output.output_file)
            if os.path.exists(output_path):
                pages.append({
                    'page': page_num,
                    'manuscript': m,
                    'output_type': 'b1',
                    'label': f'{m.file_id} B1'
                })
                page_num += 1
    
    return pages


@app.route('/evaluate/<int:page>')
def evaluate(page):
    if 'evaluator_id' not in session:
        return redirect(url_for('consent'))

    evaluator_id = session['evaluator_id']
    evaluator = Evaluator.query.get(evaluator_id)

    pages = build_page_list()
    total_pages = len(pages)

    if page < 1 or page > total_pages:
        return redirect(url_for('evaluate', page=1))

    current = pages[page - 1]
    manuscript = current['manuscript']
    output_type = current['output_type']

    evaluation = Evaluation.query.filter_by(
        evaluator_id=evaluator_id,
        manuscript_id=manuscript.id,
        output_type=output_type
    ).first()

    if not evaluation:
        evaluation = Evaluation(
            evaluator_id=evaluator_id,
            manuscript_id=manuscript.id,
            output_type=output_type,
            page_number=page
        )
        db.session.add(evaluation)
        db.session.commit()

    original_full_path = os.path.join(basedir, manuscript.original_path)
    with open(original_full_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    output_content = ""
    output = Output.query.filter_by(manuscript_id=manuscript.id, system_type=output_type).first()
    if output:
        output_path = os.path.join(basedir, 'data', f'{output_type}_outputs', output.output_file)
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                output_content = f.read()

    completed = Evaluation.query.filter_by(
        evaluator_id=evaluator_id,
        is_draft=True
    ).filter(
        Evaluation.score_kejelasan.isnot(None)
    ).count()

    # Check which output types exist for this manuscript
    available_outputs = []
    for ot in ['enip', 'b1']:
        o = Output.query.filter_by(manuscript_id=manuscript.id, system_type=ot).first()
        if o:
            op = os.path.join(basedir, 'data', f'{ot}_outputs', o.output_file)
            if os.path.exists(op):
                available_outputs.append(ot)

    return render_template('evaluate.html',
        evaluator=evaluator,
        manuscript=manuscript,
        evaluation=evaluation,
        original_content=original_content,
        output_content=output_content,
        output_type=output_type,
        page=page,
        total_pages=total_pages,
        completed=completed,
        pages=pages,
        available_outputs=available_outputs
    )


@app.route('/api/evaluation/save-draft', methods=['POST'])
def save_draft():
    data = request.json
    evaluator_id = session.get('evaluator_id')

    if not evaluator_id:
        return jsonify({'error': 'Not authenticated'}), 401

    evaluation = Evaluation.query.filter_by(
        evaluator_id=evaluator_id,
        manuscript_id=data['manuscript_id'],
        output_type=data['output_type']
    ).first()

    if not evaluation:
        evaluation = Evaluation(
            evaluator_id=evaluator_id,
            manuscript_id=data['manuscript_id'],
            output_type=data['output_type'],
            page_number=data['page_number']
        )
        db.session.add(evaluation)

    evaluation.score_kejelasan = data.get('score_kejelasan')
    evaluation.score_koherensi = data.get('score_koherensi')
    evaluation.score_kedalaman = data.get('score_kedalaman')
    evaluation.score_akurasi = data.get('score_akurasi')
    evaluation.score_gaya = data.get('score_gaya')
    evaluation.score_mekanik = data.get('score_mekanik')
    evaluation.score_engagement = data.get('score_engagement')

    evaluation.comment_kejelasan = data.get('comment_kejelasan')
    evaluation.comment_koherensi = data.get('comment_koherensi')
    evaluation.comment_kedalaman = data.get('comment_kedalaman')
    evaluation.comment_akurasi = data.get('comment_akurasi')
    evaluation.comment_gaya = data.get('comment_gaya')
    evaluation.comment_mekanik = data.get('comment_mekanik')
    evaluation.comment_engagement = data.get('comment_engagement')

    evaluation.is_draft = True

    db.session.commit()
    return jsonify({'success': True, 'message': 'Draft saved'})


@app.route('/api/evaluation/submit', methods=['POST'])
def submit_evaluation():
    data = request.json
    evaluator_id = session.get('evaluator_id')

    if not evaluator_id:
        return jsonify({'error': 'Not authenticated'}), 401

    evaluation = Evaluation.query.filter_by(
        evaluator_id=evaluator_id,
        manuscript_id=data['manuscript_id'],
        output_type=data['output_type']
    ).first()

    if evaluation:
        evaluation.score_kejelasan = data.get('score_kejelasan')
        evaluation.score_koherensi = data.get('score_koherensi')
        evaluation.score_kedalaman = data.get('score_kedalaman')
        evaluation.score_akurasi = data.get('score_akurasi')
        evaluation.score_gaya = data.get('score_gaya')
        evaluation.score_mekanik = data.get('score_mekanik')
        evaluation.score_engagement = data.get('score_engagement')

        evaluation.comment_kejelasan = data.get('comment_kejelasan')
        evaluation.comment_koherensi = data.get('comment_koherensi')
        evaluation.comment_kedalaman = data.get('comment_kedalaman')
        evaluation.comment_akurasi = data.get('comment_akurasi')
        evaluation.comment_gaya = data.get('comment_gaya')
        evaluation.comment_mekanik = data.get('comment_mekanik')
        evaluation.comment_engagement = data.get('comment_engagement')

        evaluation.is_draft = False
        evaluation.completed_at = datetime.utcnow()

        db.session.commit()
        return jsonify({'success': True, 'message': 'Evaluation submitted'})

    return jsonify({'error': 'Evaluation not found'}), 404


@app.route('/api/progress')
def get_progress():
    evaluator_id = session.get('evaluator_id')
    if not evaluator_id:
        return jsonify({'error': 'Not authenticated'}), 401

    target = len(build_page_list())
    completed = Evaluation.query.filter_by(evaluator_id=evaluator_id, is_draft=False).count()

    return jsonify({
        'total': target,
        'completed': completed,
        'percentage': (completed / target * 100) if target > 0 else 0
    })


@app.route('/api/output/<int:manuscript_id>/<output_type>')
def get_output(manuscript_id, output_type):
    if 'evaluator_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    if output_type not in ('enip', 'b1'):
        return jsonify({'error': 'Invalid output type'}), 400

    output = Output.query.filter_by(
        manuscript_id=manuscript_id,
        system_type=output_type
    ).first()

    if not output:
        return jsonify({'content': f'**Output {output_type.upper()} tidak tersedia untuk naskah ini.**', 'output_type': output_type})

    output_path = os.path.join(basedir, 'data', f'{output_type}_outputs', output.output_file)
    if not os.path.exists(output_path):
        return jsonify({'content': f'**Output {output_type.upper()} tidak tersedia untuk naskah ini.**', 'output_type': output_type})

    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return jsonify({'content': content, 'output_type': output_type})


@app.route('/api/general-comments', methods=['POST'])
def save_general_comments():
    data = request.json
    evaluator_id = session.get('evaluator_id')

    if not evaluator_id:
        return jsonify({'error': 'Not authenticated'}), 401

    comment = GeneralComment.query.filter_by(evaluator_id=evaluator_id).first()
    if not comment:
        comment = GeneralComment(evaluator_id=evaluator_id)
        db.session.add(comment)

    comment.strengths = data.get('strengths')
    comment.weaknesses = data.get('weaknesses')
    comment.suggestions = data.get('suggestions')

    db.session.commit()
    return jsonify({'success': True})


# ---------------------------------------------------------------------------
# Admin authentication
#
# The password hash is read from a bind-mounted file rather than an environment
# variable on purpose: Compose interpolates `$NAME` in both `.env` and
# `environment:` entries, which silently truncates any password hash containing
# `$` followed by a letter. Files are never interpolated, so the hash is safe
# here regardless of its contents.
#
# Generate the file with (note --entrypoint: the image ENTRYPOINT is
# entrypoint.sh, which ends in `exec gunicorn` and would never return).
# Run `docker compose build webapp` first, or BuildKit writes its progress to
# stdout and that output lands in the hash file:
#   docker compose run --rm --entrypoint python webapp -c \
#     "import getpass;from werkzeug.security import generate_password_hash;print(generate_password_hash(getpass.getpass()))" \
#     > secrets/admin_password_hash
#
# Non-interactive equivalent (CI, scripts), which keeps the password out of the
# shell history:
#   printf '%s' "$ADMIN_PW" | docker compose run --rm -T --entrypoint python webapp -c \
#     "import sys;from werkzeug.security import generate_password_hash;print(generate_password_hash(sys.stdin.read().strip()))" \
#     > secrets/admin_password_hash
#
# On PowerShell, `>` writes UTF-16, which this file is read as UTF-8; the app
# then refuses the hash and keeps /admin locked. Use Out-File -Encoding utf8, or
# write it from inside the container as above.
#
# .env must already contain SECRET_KEY: Compose interpolates the whole file
# before running anything, so the command fails without it.
# ---------------------------------------------------------------------------

ADMIN_PASSWORD_HASH_FILE = os.environ.get(
    'ADMIN_PASSWORD_HASH_FILE', '/run/secrets/admin_password_hash'
)
LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 300
# Shared by every gunicorn worker via a file: entrypoint.sh runs four workers, and
# an in-process dict would split attempts across them so the lockout never fires.
LOGIN_STATE_FILE = os.environ.get(
    'ADMIN_LOGIN_STATE_FILE', os.path.join(app.instance_path, 'admin_login_failures.json')
)


def load_admin_password_hash():
    try:
        with open(ADMIN_PASSWORD_HASH_FILE, encoding='utf-8') as handle:
            digest = handle.read().strip()
    except IsADirectoryError:
        # Docker creates a directory at the bind-mount source when the file does
        # not exist yet, so this means the hash was never generated.
        app.logger.error(
            'Admin password hash path %s is a directory, so it was never generated. '
            'Remove it and run the generate command in docker-compose.caddy.yml.',
            ADMIN_PASSWORD_HASH_FILE
        )
        return None
    except (OSError, UnicodeDecodeError):
        # Never let a bad secrets file stop the app from booting: that would take
        # the evaluator flow offline too. A shell redirect in PowerShell writes
        # UTF-16, which fails to decode as UTF-8, so this is easy to hit by accident.
        app.logger.error(
            'Admin password hash not readable as UTF-8 text at %s; /admin stays locked.',
            ADMIN_PASSWORD_HASH_FILE
        )
        return None
    if not digest:
        app.logger.error(
            'Admin password hash at %s is empty; /admin stays locked.',
            ADMIN_PASSWORD_HASH_FILE
        )
        return None
    if len(digest.split()) > 1:
        app.logger.error(
            'Admin password hash at %s contains %d lines; /admin stays locked. '
            'Regenerate it without shell redirection.',
            ADMIN_PASSWORD_HASH_FILE, len(digest.split())
        )
        return None
    return digest


ADMIN_PASSWORD_HASH = load_admin_password_hash()


def read_login_state():
    try:
        with open(LOGIN_STATE_FILE, encoding='utf-8') as handle:
            state = json.load(handle)
    except (OSError, ValueError):
        return {}
    return state if isinstance(state, dict) else {}


def write_login_state(state):
    tmp_path = LOGIN_STATE_FILE + '.tmp'
    try:
        with open(tmp_path, 'w', encoding='utf-8') as handle:
            json.dump(state, handle)
        os.replace(tmp_path, LOGIN_STATE_FILE)
    except OSError:
        app.logger.warning('could not persist admin login state', exc_info=True)


def login_locked(ip):
    now = time.time()
    entry = read_login_state().get(ip)
    if entry is None:
        return False
    failures, window_start = entry
    return failures >= LOGIN_MAX_ATTEMPTS and now - window_start <= LOGIN_LOCKOUT_SECONDS


def record_login_failure(ip):
    now = time.time()
    state = read_login_state()
    for key in [k for k, v in state.items() if now - v[1] > LOGIN_LOCKOUT_SECONDS]:
        del state[key]
    failures, window_start = state.get(ip, [0, now])
    if now - window_start > LOGIN_LOCKOUT_SECONDS:
        failures, window_start = 0, now
    state[ip] = [failures + 1, window_start]
    write_login_state(state)


def clear_login_failures(ip):
    state = read_login_state()
    if state.pop(ip, None) is not None:
        write_login_state(state)


@app.before_request
def require_admin():
    """Gate every /admin path, including the JSON and CSV exports."""
    if not request.path.startswith('/admin'):
        return None
    if request.endpoint in ('admin_login', 'admin_logout'):
        return None
    if session.get('is_admin'):
        return None
    return redirect(url_for('admin_login', next=request.path))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))

    error = None
    if request.method == 'POST':
        client_ip = request.remote_addr or 'unknown'
        if ADMIN_PASSWORD_HASH is None:
            error = 'Admin password is not configured on the server.'
        elif login_locked(client_ip):
            error = 'Terlalu banyak percobaan. Coba lagi dalam 5 menit.'
        elif check_password_hash(ADMIN_PASSWORD_HASH, request.form.get('password', '')):
            clear_login_failures(client_ip)
            session['is_admin'] = True
            session.permanent = True
            # Only ever redirect back into /admin. This also rejects
            # protocol-relative targets such as //evil.example.
            target = request.args.get('next', '')
            if not target.startswith('/admin'):
                target = url_for('admin_dashboard')
            return redirect(target)
        else:
            record_login_failure(client_ip)
            error = 'Password salah.'

    return render_template('admin_login.html', error=error), (401 if error else 200)


@app.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    # Pop only the admin flag: session.clear() would also drop evaluator_id.
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))


@app.route('/admin/evaluations')
def admin_evaluations():
    """Export all evaluation data as JSON for admin."""
    evaluations = Evaluation.query.all()
    data = []
    for e in evaluations:
        data.append({
            'evaluator_id': e.evaluator_id,
            'manuscript_id': e.manuscript_id,
            'output_type': e.output_type,
            'page_number': e.page_number,
            'is_draft': e.is_draft,
            'completed_at': e.completed_at.isoformat() if e.completed_at else None,
            'score_kejelasan': e.score_kejelasan,
            'score_koherensi': e.score_koherensi,
            'score_kedalaman': e.score_kedalaman,
            'score_akurasi': e.score_akurasi,
            'score_gaya': e.score_gaya,
            'score_mekanik': e.score_mekanik,
            'score_engagement': e.score_engagement,
            'comment_kejelasan': e.comment_kejelasan,
            'comment_koherensi': e.comment_koherensi,
            'comment_kedalaman': e.comment_kedalaman,
            'comment_akurasi': e.comment_akurasi,
            'comment_gaya': e.comment_gaya,
            'comment_mekanik': e.comment_mekanik,
            'comment_engagement': e.comment_engagement
        })
    return jsonify(data)


@app.route('/admin/evaluations/csv')
def admin_evaluations_csv():
    """Export all evaluation data as CSV for admin."""
    import csv
    import io
    
    evaluations = Evaluation.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        'evaluator_id', 'manuscript_id', 'output_type', 'page_number', 'is_draft', 'completed_at',
        'score_kejelasan', 'score_koherensi', 'score_kedalaman', 'score_akurasi', 'score_gaya', 'score_mekanik', 'score_engagement',
        'comment_kejelasan', 'comment_koherensi', 'comment_kedalaman', 'comment_akurasi', 'comment_gaya', 'comment_mekanik', 'comment_engagement'
    ])
    
    for e in evaluations:
        writer.writerow([
            e.evaluator_id, e.manuscript_id, e.output_type, e.page_number, e.is_draft,
            e.completed_at.isoformat() if e.completed_at else None,
            e.score_kejelasan, e.score_koherensi, e.score_kedalaman, e.score_akurasi, e.score_gaya, e.score_mekanik, e.score_engagement,
            e.comment_kejelasan, e.comment_koherensi, e.comment_kedalaman, e.comment_akurasi, e.comment_gaya, e.comment_mekanik, e.comment_engagement
        ])
    
    response = app.response_class(
        response=output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=evaluations.csv'}
    )
    return response


@app.route('/admin')
def admin_dashboard():
    """Admin dashboard to view all evaluators and their progress."""
    evaluators = Evaluator.query.all()
    target = len(build_page_list())
    stats = []
    for ev in evaluators:
        total = Evaluation.query.filter_by(evaluator_id=ev.id).count()
        submitted = Evaluation.query.filter_by(evaluator_id=ev.id, is_draft=False).count()
        stats.append({
            'id': ev.id,
            'name': ev.name,
            'created_at': ev.created_at.strftime('%Y-%m-%d %H:%M') if ev.created_at else '-',
            'total': total,
            'target': target,
            'submitted': submitted
        })
    return render_template('admin.html', evaluators=stats, target=target)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)
