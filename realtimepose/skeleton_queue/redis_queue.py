
from typing import Tuple
import numpy as np
from constants.constants import QUEUE_NAME
from skeleton_queue.skeleton_queue import SkeletonQueue
import redis
import json

class RedisQueue(SkeletonQueue):
    
    def __init__(self) -> None:
        super().__init__()
        self.channel = redis.Redis(host='localhost', port=6379, db=0)
        
    def get_data(self) -> np.ndarray:
        data = self.channel.get_message()
        if data is not None:
            body = data["data"]
        try:
            return(np.array(json.loads(body)))
        except:
            return(None)

    
    def push_data(self, pose: np.ndarray) -> None:
        # Redis logic
        self.channel.publish(QUEUE_NAME, json.dumps(pose.tolist()))

    def prepare_to_recieve(self) -> None:
        self.channel = self.channel.pubsub()
        self.channel.subscribe(QUEUE_NAME)
