#!/usr/bin/env python3

from faker import Faker
from app import app
from models import db, Newsletter

with app.app_context():
    fake = Faker()

    # Delete all existing records
    Newsletter.query.delete()

    # Add new records
    newsletters = []
    for i in range(50):
        newsletter = Newsletter(
            title=fake.text(max_nb_chars=20),
            body=fake.paragraph(nb_sentences=5),
        )
        newsletters.append(newsletter)

    db.session.add_all(newsletters)
    db.session.commit()
