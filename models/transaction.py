from models.share import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.String(100), nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    stripeSessionId = db.Column(db.String(700), nullable=True)
    token = db.Column(db.String(500), nullable=False)
    createdTime = db.Column(db.DateTime, nullable=False,
    default=datetime.utcnow)
    updatedTime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
