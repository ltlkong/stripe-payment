import stripe
from os import getenv

class StripeClient:
    def __init__(self):
        stripe.api_key = getenv('STRIPE_API_KEY')

    def create_checkout_session(self, orderId, currency, amount):
        try:
            order = self.__create_stripe_order(orderId)

            price = self.__create_price(order.id, currency, amount)

            checkout = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=getenv('DOMAIN')+getenv('STRIPE_PAYMENT_CALLBACK_URI')+'?orderId='+orderId,
                cancel_url=getenv("DOMAIN")+getenv('STRIPE_PAYMENT_CALLBACK_URI')+'?orderId='+orderId,
            )

            return checkout
        except Exception as e:
            print(e)

            return None
    
    def retrieve_checkout(self,checkoutId):
        return stripe.checkout.Session.retrieve(checkoutId)

    def __create_price(self,stripeOrderId, currency, amount):
        price = stripe.Price.create(
            unit_amount=amount,
            currency=currency,
            product=stripeOrderId,
        )

        return price

    def __create_stripe_order(self,orderId):
        return stripe.Product.create(name=orderId)
    
