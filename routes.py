from resources.paymentResource import PaymentResource

def init_routes(api):
    api.add_resource(PaymentResource, '/payment')
