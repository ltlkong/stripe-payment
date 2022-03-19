import stripe
from os import getenv

class StripeClient:
    def __init__(self):
        stripe.api_key = getenv('STRIPE_API_KEY')

    def createCheckoutSession(self, orderId, currency, amount,token, methods):
        try:
            order = self._createStripeOrder(orderId)

            price = self._createPrice(order.id, currency, amount)

            checkout = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                payment_method_types=methods,
                success_url=getenv('STRIPE_PAYMENT_CALLBACK_URL')+'?token='+token,
                cancel_url=getenv('STRIPE_PAYMENT_CALLBACK_URL')+'?token='+token,
            )
        except Exception as e:
            print(e)

            return None, str(e)

        return checkout, 'success'
    
    def retrieveCheckout(self,checkoutId):
        try:
            return stripe.checkout.Session.retrieve(checkoutId)
        except Exception as e:
            print(e)

            return None
    
    def retrievePaymentMethod(self,paymentIntentId):
        try:
            paymentIntent = stripe.PaymentIntent.retrieve(paymentIntentId)

            return stripe.PaymentMethod.retrieve(paymentIntent['payment_method'])
        except Exception as e:
            print(e)

            return None

    def _createPrice(self,stripeOrderId, currency, amount):
        price = stripe.Price.create(
            unit_amount=amount,
            currency=currency,
            product=stripeOrderId,
        )

        return price

    def _createStripeOrder(self,orderId):
        return stripe.Product.create(name=orderId)