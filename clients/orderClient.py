import requests

class OrderClient:
    baseUrl = 'https://jsonplaceholder.typicode.com/todos/'

    def get(self):
        order  = requests.get(self.baseUrl).json()

        return order
    
