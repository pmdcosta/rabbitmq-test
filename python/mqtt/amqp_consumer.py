#!/usr/bin/env python
import pika
from pika.credentials import ExternalCredentials


# Whenever a message is received, this function is called
def callback(ch, method, properties, body):
    #print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Setup connection
ssl_option = {'certfile': '/home/pmdcosta/DockerProjects/rabbitmq-test/ssl/pmdcosta/cert.pem',
              'keyfile': '/home/pmdcosta/DockerProjects/rabbitmq-test/ssl/pmdcosta/key.pem'}

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='server', port=5671, credentials=ExternalCredentials(), ssl=True,
                              ssl_options=ssl_option))
channel = connection.channel()

# Create a temporary queue with random name
result = channel.queue_declare(queue='consumer1', durable=True)
queue_name = result.method.queue

# Bind the queue to the exchange
channel.queue_bind(exchange='amq.topic', queue=queue_name, routing_key="reports")

# Receive message from queue and execute call callback function
channel.basic_consume(callback, queue=queue_name)

# Never ending loop waiting for messages
print(' [*] Waiting for messages. To exit press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Shutting Down...")
    channel.close()
