# !/bin/bash

# Shell script to run the docker image
docker build -t carmenlee2020/payment-service .
docker run -it -p 5001:5001 carmenlee2020/payment-service

# docker-compose up

