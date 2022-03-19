from os import stat
from tabnanny import check
from flask_restful import Resource, reqparse
from clients.stripeClient import StripeClient
from clients.orderClient import OrderClient
from services.transactionService import TransactionService

class PaymentResource(Resource):
    def __init__(self):
        self.stripeClient = StripeClient()
        self.parser = reqparse.RequestParser()
        self.transactionService = TransactionService()
        self.orderClient = OrderClient()
    
    def get(self):
        # Getting the data from the request
        parser = self.parser

        parser.add_argument('token', type=str)
        args = parser.parse_args()

        # Retrieving the transaction from database
        transaction= self.transactionService.getTransactionByToken(args['token'])

        if transaction is None:
            return {'message':'Transaction not found'},404

        # Retrieving the object from stripe api
        checkout = self.stripeClient.retrieveCheckout(transaction.stripeSessionId)

        if checkout is None:
            return {'message':'Error retrieve payment session'},500
        
        # Enum open, expired, complete
        status= checkout['status']

        if status != 'complete':
            return {'order_id':transaction.orderId, 'payment_url':checkout['url'], 'status':status, 'payment':None},200

        payment = self.stripeClient.retrievePaymentMethod(checkout['payment_intent'])

        if payment is None:
            return {'message':'Error retrieve payment'},500

        # Preparing the data
        paymentMethod = payment['type']
        paymentAmount = checkout['amount_total']
        paymentCurrency = checkout['currency']

        # Updating the order status
        self.orderClient.updateOrderStatus(transaction.orderId, status)

        return {
            'order_id': transaction.orderId,
            'status': status,
            'payment': {
                'method':paymentMethod,
                'amount':paymentAmount,
                'currency':paymentCurrency,
                'status':checkout['payment_status'], # Enum paid, unpaid
            },
            'payment_url': checkout['url'],
            'expires_at': checkout['expires_at'],
        }


    def post(self):
        # Getting the data from the request
        parser = self.parser

        parser.add_argument('orderId', type=str)
        parser.add_argument('currency', type=str)
        parser.add_argument('amount', type=int)
        args = parser.parse_args()

        # Store transaction in database
        transaction = self.transactionService.createTransaction(orderId=args['orderId'])

        if transaction is None:
            return {'message':'Error creating transaction'},500

        # Creating the checkout session from stripe api
        sessionResponse  = self.stripeClient.createCheckoutSession(args['orderId'], args['currency'], args['amount'], transaction.token, ['card', 'alipay'])

        checkout =sessionResponse[0]
        sessionMessage = sessionResponse[1]

        if checkout is None:
            return {'message': sessionMessage},500
        
        self.transactionService.updateSessionId(transaction, checkout['id'])

        return {
            'order_id': args['orderId'],
            'payment_url': checkout['url'],
            'expires_at': checkout['expires_at'],
            'token': transaction.token,
            'status': checkout['status'],
            } , 201
         
