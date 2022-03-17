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
                success_url=getenv('DOMAIN')+getenv('STRIPE_PAYMENT_CALLBACK_URI')+'?token='+token,
                cancel_url=getenv("DOMAIN")+getenv('STRIPE_PAYMENT_CALLBACK_URI')+'?token='+token,
            )
        except Exception as e:
            print(e)

            return None, str(e)

        return checkout, 'success'
    
    def retrieveCheckout(self,checkoutId):
        return stripe.checkout.Session.retrieve(checkoutId)
    
    def retrievePaymentMethod(self,paymentIntentId):
        paymentIntent = stripe.PaymentIntent.retrieve(paymentIntentId)

        return stripe.PaymentMethod.retrieve(paymentIntent['payment_method'])

    def _createPrice(self,stripeOrderId, currency, amount):
        price = stripe.Price.create(
            unit_amount=amount,
            currency=currency,
            product=stripeOrderId,
        )

        return price

    def _createStripeOrder(self,orderId):
        return stripe.Product.create(name=orderId)
    
