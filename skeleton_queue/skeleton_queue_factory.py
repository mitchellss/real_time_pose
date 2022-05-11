

from skeleton_queue.rabbitmq_queue import RabbitMQQueue
from skeleton_queue.redis_queue import RedisQueue
from skeleton_queue.skeleton_queue import SkeletonQueue


class SkeletonQueueFactory():
    
    def get_skeleton_queue(self, queue_name: str) -> SkeletonQueue:
        if queue_name == "redis":
            return RedisQueue()
        elif queue_name == "rabbitmq":
            return RabbitMQQueue()