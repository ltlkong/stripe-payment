import requests

class OrderClient:
    baseUrl = 'https://jsonplaceholder.typicode.com/todos/'

    def getOrderById(self, orderId):
        order  = requests.get(self.baseUrl).json()

        return { 
            "code": 200, 
            "data": { 
                "cust_id": "1", 
                "date_created": "Fri, 12 Jun 2020 02:14:55 GMT", 
                "delivery_address": "Singapore", 
                "modified": "Wed, 16 Mar 2022 16:29:40 GMT", 
                "order_id": 1, 
                "order_item": [ 
                    { 
                        "item_id": 1, 
                        "order_id": 1, 
                        "product_id": "1", 
                        "quantity": "1" 
                    }, 
                    { 
                        "item_id": 2, 
                        "order_id": 1, 
                        "product_id": "1", 
                        "quantity": "1" 
                    } 
                ], 
                "status": "3", 
                "total_price": 899.98 
        } 
}
    
