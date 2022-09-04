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
        logger.setLevel(mp.SUBDEBUG)

        p = mp.Process(target=self.update_pose,
                       args=[self.pose_input, self.pose])
        p.start()

        # print(self.pose_input.get_pose())

        try:
            self.frontend.new_gui()
            self.update_ui()
        except:
            pass
            p.kill()

        p.join()

    def update_pose(self, poseinput, poseabc):
        """test"""
        while True:
            pose_list = poseinput.get_pose().flatten().tolist()
            for i in range(0, len(pose_list)):
                poseabc[i] = pose_list[i] * 450 + 600

    def update_ui(self):
        """Test"""
        while True:
            self.frontend.clear()
            for component in self.scenes[self.active_scene].components:
                if isinstance(component, Skeleton):
                    # logging.warning("Setting new skeleton points")
                    component.skeleton_points = np.array(
                        self.pose.get_obj()).reshape((33, 4))
                    # logging.warning(component.skeleton_points)

                component.render(self.frontend.window)

            self.frontend.update()
