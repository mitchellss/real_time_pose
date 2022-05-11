
from constants.constants import QUEUE_NAME
from skeleton_queue.skeleton_queue import SkeletonQueue
import numpy as np
import pika
import json

class RabbitMQQueue(SkeletonQueue):
    
    def __init__(self) -> None:
        super().__init__()
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME, durable=False, auto_delete=True, arguments={'x-max-length' : 10, 'no_ack': True})

        
    def get_data(self) -> np.ndarray:
        return super().get_data()
    
    def push_data(self, pose: np.ndarray) -> None:
        # RabbitMQ logic
        self.channel.basic_publish(exchange='',
                                    routing_key=QUEUE_NAME,
                                    body=json.dumps(pose.tolist()))
        return super().push_data()
