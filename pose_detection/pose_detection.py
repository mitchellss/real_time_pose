import json
import numpy as np
import pika

from constants.constants import QUEUE_NAME

class PoseDetection:

    def __init__(self) -> None:
        self.pose: np.ndarray = None
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()

        self.channel.queue_declare(queue=QUEUE_NAME, durable=False, auto_delete=True, arguments={'x-max-length' : 10, 'no_ack': True})

    def add_pose_to_queue(self) -> None:
        # RabbitMQ logic
        self.channel.basic_publish(exchange='',
                                    routing_key=QUEUE_NAME,
                                    body=json.dumps(self.pose.tolist()))