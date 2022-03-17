from turtle import st
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
        stripeSession = self.stripeClient.retrieveCheckout(transaction.stripeSessionId)

        if stripeSession is None:
            return {'message':'Error retrieve payment session'},500

        payment = self.stripeClient.retrievePaymentMethod(stripeSession['payment_intent'])

        if payment is None:
            return {'message':'Error retrieve payment'},500

        # Preparing the data
        status= stripeSession['status']
        paymentMethod = payment['type']
        paymentAmount = stripeSession['amount_total']
        paymentCurrency = stripeSession['currency']

        # Updating the order status
        self.orderClient.updateOrderStatus(transaction.orderId, status)

        return {
            'order_id': transaction.orderId,
            'status': status,
            'payment': {
                'method':paymentMethod,
                'amount':paymentAmount,
                'currency':paymentCurrency,
            }
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
            'payment_url': checkout.url,
            } , 201
         
