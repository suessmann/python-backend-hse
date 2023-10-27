# Homework 4

Super simple project with 1 consumer and 2 producers
using Celery and Rabbit MQ.

### Requirements

1) Local RabbitMQ instance on default port
2) Celery installed - `pip install celery`

### How to run consumer

`celery -A tasks worker --loglevel=info`

### How to run task producer

`python worker1.py` for task #1
`python worker2.py` for task #2
