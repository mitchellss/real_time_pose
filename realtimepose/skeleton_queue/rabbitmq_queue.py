
from typing import Tuple
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
        _, _, body = self.channel.basic_get(queue=QUEUE_NAME)
        try:
            return(np.array(json.loads(body)))
        except:
            return(None)
        
    def push_data(self, pose: np.ndarray) -> None:
        # RabbitMQ logic
        self.channel.basic_publish(exchange='',
                                    routing_key=QUEUE_NAME,
                                    body=json.dumps(pose.tolist()))

    def prepare_to_recieve(self) -> None:
        self.channel.queue_purge(queue=QUEUE_NAME)
        self.channel.basic_qos(prefetch_count=1)
