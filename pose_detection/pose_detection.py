import json
import numpy as np
import pika
import redis

from constants.constants import QUEUE_NAME

class PoseDetection:

    def __init__(self, queue) -> None:
        self.pose: np.ndarray = None
        self.queue = queue
        if self.queue == "rabbitmq":
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = connection.channel()
            self.channel.queue_declare(queue=QUEUE_NAME, durable=False, auto_delete=True, arguments={'x-max-length' : 10, 'no_ack': True})
        elif self.queue == "redis":
            self.channel = redis.Redis(host='localhost', port=6379, db=0)


    def add_pose_to_queue(self) -> bool:
        if self.queue == "rabbitmq":
            # RabbitMQ logic
            self.channel.basic_publish(exchange='',
                                        routing_key=QUEUE_NAME,
                                        body=json.dumps(self.pose.tolist()))
        elif self.queue == "redis":
            # Redis logic
            self.channel.publish(QUEUE_NAME, json.dumps(self.pose.tolist()))
