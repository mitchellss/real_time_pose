
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
        return super().get_data()
    
    def push_data(self, pose: np.ndarray) -> None:
        # Redis logic
        self.channel.publish(QUEUE_NAME, json.dumps(pose.tolist()))
        return super().push_data()