from models.share import db
from models.transaction import Transaction
from datetime import datetime
from common.uuidUtil import UuidUtil

class TransactionService:
    def __init__(self):
        self.uuidUtil = UuidUtil()

    def getTransactionByOrderId(self, orderId):
        transaction = db.session.query(Transaction).filter_by(orderId=orderId).first()
        return transaction

    def getTransactionByToken(self, token):
        transaction = db.session.query(Transaction).filter_by(token=token).first()
        return transaction

    def updateTransactionStatus(self, transaction, newStatus):
        if transaction.status != newStatus:
            transaction.updatedTime = datetime.now()
        transaction.status = newStatus
        db.session.commit()

    def createTransaction(self, orderId, amount, currency):
        transaction = Transaction(orderId=orderId, amount=amount, currency=currency, status='open', token=self.uuidUtil.generateUUID())
        db.session.add(transaction)
        db.session.commit()

        return transaction
    
    def updateSessionId(self, transaction, stripeSessionId):
        transaction.stripeSessionId = stripeSessionId
        db.session.commit()
    
    def updateToken(self, transaction):
        transaction.token = self.uuidUtil.generateUUID()
        db.session.commit()