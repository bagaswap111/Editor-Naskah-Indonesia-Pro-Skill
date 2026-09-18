import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'enip-eval-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'evaluations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    total = Evaluation.query.filter_by(evaluator_id=evaluator_id).count()
    completed = Evaluation.query.filter_by(evaluator_id=evaluator_id, is_draft=False).count()

    return jsonify({
        'total': total,
        'completed': completed,
        'percentage': (completed / 30 * 100) if total > 0 else 0
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
    stats = []
    for ev in evaluators:
        total = Evaluation.query.filter_by(evaluator_id=ev.id).count()
        submitted = Evaluation.query.filter_by(evaluator_id=ev.id, is_draft=False).count()
        stats.append({
            'id': ev.id,
            'name': ev.name,
            'created_at': ev.created_at.strftime('%Y-%m-%d %H:%M') if ev.created_at else '-',
            'total': total,
            'submitted': submitted
        })
    return render_template('admin.html', evaluators=stats)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)
