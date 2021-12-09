#!/bin/bash

env LOCUST_ENDPOINT=/async/http/sync/ locust -f agent.py \
--host http://127.0.0.1:4242 \
--users 500 \
--spawn-rate 50 \
--run-time 60s \
--headless

