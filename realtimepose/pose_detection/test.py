import time
import pika

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue=QUEUE_NAME, durable=False)
# print(' [*] Waiting for messages. To exit press CTRL+C')

# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     print(body)
#     print(f" [x] Done {time.time()}")
#     ch.basic_ack(delivery_tag = method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
# channel.basic_consume(QUEUE_NAME, callback)

# channel.start_consuming()

import redis

r = redis.Redis(host='localhost', port=6379, db=0)

p = r.pubsub()

p.subscribe("skeleton_queue")

while True:
  message = p.get_message()
  if message:
    print(f"{message} {time.time()}")
