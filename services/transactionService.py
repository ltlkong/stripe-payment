from models.share import db
from models.transaction import Transaction
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

    def createTransaction(self, orderId):
        transaction = Transaction(orderId=orderId,token=self.uuidUtil.generateUUID())

        try:
            db.session.add(transaction)
            db.session.commit()

            return transaction
        except Exception as e:
            print(e)
            db.session.rollback()

            return None

    
    def updateSessionId(self, transaction, stripeSessionId):
        transaction.stripeSessionId = stripeSessionId
        db.session.commit()
    
    def updateToken(self, transaction):
        transaction.token = self.uuidUtil.generateUUID()
        db.session.commit()