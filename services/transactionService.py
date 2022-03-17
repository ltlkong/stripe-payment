from models.share import db
from models.transaction import Transaction
from datetime import datetime

class TransactionService:
    def getTransactionByOrderId(self, orderId):
        transaction = db.session.query(Transaction).filter_by(orderId=orderId).first()
        return transaction

    def updateTransactionStatus(self, transaction, newStatus):
        if transaction.status != newStatus:
            transaction.updatedTime = datetime.now()
        transaction.status = newStatus
        db.session.commit()

    def createTransaction(self, orderId, amount, currency, stripeSessionId):
        transaction = Transaction(orderId=orderId, amount=amount, currency=currency, status='pending', stripeSessionId=stripeSessionId)
        db.session.add(transaction)
        db.session.commit()