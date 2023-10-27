from celery import Celery

# Create a Celery instance with connection to local RabbitMq instance
app = Celery('tasks', broker='pyamqp://guest@localhost//')


# Define the tasks
@app.task
def process_task1():
    # Task 1 logic here
    print("Processing Task 1")


@app.task
def process_task2():
    # Task 2 logic here
    print("Processing Task 2")
