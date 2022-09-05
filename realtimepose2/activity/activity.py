"""Test"""
from typing import List

import numpy as np

import multiprocessing as mp
import logging

from realtimepose2.activity.scene import Scene
from realtimepose2.core.displaying import UserInterface
from realtimepose2.core.displaying.components import Skeleton
from realtimepose2.core.recieving import PoseGenerator


class Activity:
    """Test"""

    scenes: List[Scene] = []
    active_scene: int = 0
    pose = mp.Array("d", 33*4)

    def __init__(self, pose_input: PoseGenerator, frontend: UserInterface) -> None:
        self.pose_input = pose_input
        self.frontend = frontend

    def add_scene(self, scene: Scene):
        """Test"""
        self.scenes.append(scene)

    def run(self):
        """Test"""
        logger = mp.log_to_stderr()
        logger.setLevel(mp.SUBDEBUG)  # type: ignore

        p = mp.Process(target=self.update_ui,
                       args=[self.frontend, self.scenes, self.pose])
        p.start()

        # print(self.pose_input.get_pose())

        try:
            self.update_pose()
        except Exception as e:
            logging.error(e)
            p.kill()

        p.join()

    def update_pose(self):
        """test"""
        while True:
            pose = self.pose_input.get_pose()
            pose_list = pose.flatten().tolist()
            # logging.warning(pose_list)
            for i in range(0, len(pose_list)):
                self.pose[i] = pose_list[i] * 450 + 600

    def update_ui(self, frontend: UserInterface, scenes: List[Scene], pose):
        """Test"""
        try:
            frontend.new_gui()
        except Exception as e:
            logging.error(str(e))
        try:
            while True:
                frontend.clear()
                for component in scenes[0].components:
                    if isinstance(component, Skeleton):
                        # logging.warning("Setting new skeleton points")
                        component.skeleton_points = np.array(self.pose.get_obj()).reshape((33, 4))
                        # logging.warning(component.skeleton_points)

                    component.render(frontend.window)

                frontend.update()
        except Exception as e:
            logging.error(str(e))
