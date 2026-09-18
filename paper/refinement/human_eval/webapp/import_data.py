import os
from app import app, db, Manuscript, Output

MANUSCRIPTS = [
    {"file_id": "aca_01", "style": "Akademis", "type": "injected"},
    {"file_id": "aca_03", "style": "Akademis", "type": "clean"},
    {"file_id": "jur_01", "style": "Jurnalistik", "type": "injected"},
    {"file_id": "jur_03", "style": "Jurnalistik", "type": "clean"},
    {"file_id": "pop_01", "style": "Populer-Edukatif", "type": "injected"},
    {"file_id": "pop_03", "style": "Populer-Edukatif", "type": "clean"},
    {"file_id": "per_01", "style": "Persuasif", "type": "injected"},
    {"file_id": "per_03", "style": "Persuasif", "type": "clean"},
    {"file_id": "bkl_01_01", "style": "Populer-Edukatif", "type": "natural"},
    {"file_id": "bkl_08_01", "style": "Akademis", "type": "natural"},
]

OUTPUT_MAPPING = {
    "aca_01": "OUT-0001.md",
    "aca_03": "OUT-0002.md",
    "jur_01": "OUT-0003.md",
    "jur_03": "OUT-0004.md",
    "pop_01": "OUT-0005.md",
    "pop_03": "OUT-0006.md",
    "per_01": "OUT-0007.md",
    "per_03": "OUT-0008.md",
    "bkl_01_01": "OUT-0009.md",
    "bkl_08_01": "OUT-0010.md",
}

B1_MAPPING = {
    "aca_01": "OUT-0011.md",
    "aca_03": "OUT-0012.md",
    "jur_01": "OUT-0013.md",
    "jur_03": "OUT-0014.md",
    "pop_01": "OUT-0015.md",
}

with app.app_context():
    Output.query.delete()
    Manuscript.query.delete()
    db.session.commit()

    for m in MANUSCRIPTS:
        manuscript = Manuscript(
            file_id=m["file_id"],
            style=m["style"],
            manuscript_type=m["type"],
            original_path="data/manuscripts/{}.txt".format(m["file_id"])
        )
        db.session.add(manuscript)

    db.session.commit()

    for manuscript in Manuscript.query.all():
        enip_output = Output(
            manuscript_id=manuscript.id,
            system_type="enip",
            output_file=OUTPUT_MAPPING[manuscript.file_id]
        )
        db.session.add(enip_output)

        if manuscript.file_id in B1_MAPPING:
            b1_output = Output(
                manuscript_id=manuscript.id,
                system_type="b1",
                output_file=B1_MAPPING[manuscript.file_id]
            )
            db.session.add(b1_output)

    db.session.commit()
    print("Imported {} manuscripts and their outputs!".format(len(MANUSCRIPTS)))
