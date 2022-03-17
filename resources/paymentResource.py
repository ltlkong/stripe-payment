from flask_restful import Resource, reqparse
from clients.stripeClient import StripeClient
from uuid import uuid4
from models.transaction import Transaction
from services.transactionService import TransactionService

class PaymentResource(Resource):
    def __init__(self):
        self.stripeClient = StripeClient()
        self.parser = reqparse.RequestParser()
        self.transactionService = TransactionService()
    
    def get(self):
        # Getting the data from the request
        parser = self.parser

        parser.add_argument('orderId', type=str)
        args = parser.parse_args()

        # Retrieving the transaction from database
        transaction= self.transactionService.getTransactionByOrderId(args['orderId'])

        if transaction is None:
            return {'message':'Transaction not found'},404

        # Retrieving the checkout session from stripe api
        stripeSession = self.stripeClient.retrieve_checkout(transaction.stripeSessionId)
        
        self.transactionService.updateTransactionStatus(transaction, stripeSession['status'])

        return {
            'orderId': transaction.orderId,
            'status': transaction.status,
        }


    def post(self):
        # Getting the data from the request
        parser = self.parser

        parser.add_argument('orderId', type=str)
        parser.add_argument('currency', type=str)
        parser.add_argument('amount', type=int)
        args = parser.parse_args()

        # Creating the checkout session from stripe api
        checkout  = self.stripeClient.create_checkout_session(args['orderId'], args['currency'], args['amount'])

        if checkout is None:
            return {'message':'Error creating checkout session'},500

        # Store transaction in database
        transaction = self.transactionService.createTransaction(orderId=args['orderId'], amount=args['amount'], currency=args['currency'], stripeSessionId=checkout['id'])

        return {
            'orderId': args['orderId'],
            'method':'card',
            'payment_url': checkout.url,
            } 
         
