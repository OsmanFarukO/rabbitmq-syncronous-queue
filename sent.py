#!/usr/bin/env python3
# This script can help you sync your rabbbitmq queues each other
import pika

SEND_HOST="a"
SEND_PORT=5672
RECEIVE_HOST="b"
RECEIVE_PORT=5672
QUEUE="x"
credentials = pika.PlainCredentials('user', 'password')

sent_connection = pika.BlockingConnection(pika.ConnectionParameters(SEND_HOST, SEND_PORT, '/', credentials))
global sent_channel
sent_channel = sent_connection.channel()
# sent_connection.close()

receive_connection = pika.BlockingConnection(pika.ConnectionParameters(RECEIVE_HOST, RECEIVE_PORT, '/', credentials))
receive_channel = receive_connection.channel()

def sent_to(body):
    sent_channel.queue_declare(queue=QUEUE)
    sent_channel.basic_publish(exchange="", routing_key=QUEUE, body=body)
    print(" [x] Sended %r" % body)

def receive_callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    sent_to(body)

receive_channel.queue_declare(queue=QUEUE)
print(" [*] Waiting for messages. To exit press Ctrl+C")
receive_channel.basic_consume(queue=QUEUE, on_message_callback=receive_callback)
receive_channel.start_consuming()
