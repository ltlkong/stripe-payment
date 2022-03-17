# TODO: Create db


from app import db,app

import models.transaction

with app.app_context():
    db.create_all()
