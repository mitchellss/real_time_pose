
import numpy as np
from skeleton_queue.skeleton_queue import SkeletonQueue


class RedisQueue(SkeletonQueue):
    
    def __init__(self) -> None:
        super().__init__()
        
    def get_data(self) -> np.ndarray:
        return super().get_data()
    
    def push_data(self) -> np.ndarray:
        return super().push_data()