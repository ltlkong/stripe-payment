# Payment service

[stripe]('https://stripe.com/en-ca') implementation


## Start the project

1. Create a payment database
2. Config env and docker compose
3. Run ./run.sh
4. Run migrate.py

## Domain

[http://127.0.0.1:5001/api/v1/payment](http://127.0.0.1:5001/api/v1/payment)

## File structure

- app.py (app)
- routes.py (All routes)
- clients/ (Http clients)
- services/ (Business logic layer)
- models/ (Data models)
- common/ (Util classes)
- resources/ (Controllers deal with requests)
