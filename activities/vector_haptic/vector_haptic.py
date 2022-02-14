
import numpy as np
from activities.activity import Activity
from activities.vector_haptic.haptic_mapping import find_intensity_array, make_message
from constants.constants import *
from ui.pygame.pygame_button import PyGameButton
from ui.pygame.pygame_hand_bubble import PyGameHandBubble
from ui.pygame.pygame_skeleton import PyGameSkeleton
from playsound import playsound
import random
import threading

from ui.pygame.pygame_text import PyGameText
from ui.pygame.pygame_timer import PyGameTimer

import socket


class VectorHaptic(Activity):

    TCP_IP = "172.16.1.2"

    TCP_PORT = 8888
    
    MOTORS = np.array([np.array([0,0,1]), np.array([0,0,-1]), np.array([0,-1,0]), np.array([0,1,0])]) #array of motor positions

    def __init__(self, body_point_array, **kwargs) -> None:
        super().__init__(body_point_array, **kwargs)
        self.persist = {}
        self.persist[SKELETON] = PyGameSkeleton(body_point_array)
        self.persist[TIMER] = PyGameTimer(0.3, -1.2, func=self.time_expire_func)

        stage_0 = {}
        stage_0["target_1"] = PyGameButton(50, (255, 0, 0, 120), random.uniform(-0.7, 0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0, -0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET, precision=50, func=self.target_1_func, target_pts=[16])
        stage_0["bubble_1"] = PyGameHandBubble(0, 0, 16, 30, (255, 0, 0, 120))

        self.stages = [stage_0]
        self.stage = 0

        self.components = self.stages[self.stage]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))

        mode = "push"

        pattern = '118'
        if mode == "push":
            self.commands = {'up':f'/buz2/{pattern}', 'down':f'/buz0/{pattern}', 'left':f'/buz1/{pattern}', 'right':f'/buz3/{pattern}key'}

        if mode == "pull":
            self.commands = {'up':f'/buz0/{pattern}', 'down':f'/buz2/{pattern}', 'left':f'/buz3/{pattern}', 'right':f'/buz1/{pattern}'}

        self.index = 0

        self.current_pos = np.array([0,0,0]) #Current Pos
        self.goal_position = np.array([0,1,1]) # Goal Pos


    def time_expire_func(self) -> None:
        self.stage = 0
        self.change_stage()
        if STOP_LOGGING in self.funcs:
            for func in self.funcs[STOP_LOGGING]:
                func()
    
    def target_1_func(self) -> None:
        old_coords = (self.stages[0]["target_1"].x_pos, self.stages[0]["target_1"].y_pos)
        new_coords = (random.uniform(-0.7,0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0,-0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET)
        while old_coords[0] - new_coords[0] < 0.1 and old_coords[1] - new_coords[1] < 0.1:
            new_coords = (random.uniform(-0.7,0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0,-0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET)
        
        self.stages[0]["target_1"].set_pos(new_coords[0], new_coords[1])
        self.alert()

    def handle_frame(self, **kwargs) -> None:
        super().handle_frame(**kwargs)

        self.index += 1

        self.current_pos = np.array([0, self.persist[SKELETON].skeleton_array[16][0], self.persist[SKELETON].skeleton_array[16][1]]) #Current Pos
        self.goal_position = np.array([0, self.stages[0]["target_1"].x_pos, self.stages[0]["target_1"].y_pos])

        intensity = find_intensity_array(self.current_pos, self.goal_position, self.MOTORS)
        print(self.goal_position, intensity)
        message = make_message(intensity)

        for _ in range(0,10):
            self.s.send(f'{message}\n'.encode('ascii'))

        self.change_stage()

    def alert(self):
        threading.Thread(target=playsound, args=(PATH / "activities/vector_haptic/beep.mp3",), daemon=True).start()
