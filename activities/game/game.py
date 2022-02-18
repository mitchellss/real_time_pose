
from activities.activity import Activity
from constants.constants import *
from ui.components.component_factory import ComponentFactory
import random
from utils.utils import *


class Game(Activity):

    def __init__(self, body_point_array, ui, **kwargs) -> None:
        super().__init__(body_point_array, ui, **kwargs)

        cf = ComponentFactory(self.ui)

        self.persist = {}
        self.persist[SKELETON] = cf.new_skeleton(body_point_array)
        self.persist[TIMER] = cf.new_timer(300, 50, func=self.time_expire_func)

        stage_0 = {}
        stage_0[START_TARGET] = cf.new_button(50, (0, 255, 0, 120), bp2p_x(0), bp2p_y(-0.6), precision=50, func=self.start_button_func, target_pts=[16, 15])

        stage_1 = {}
        stage_1["target_1"] = cf.new_button(50, (255, 0, 0, 120), random.uniform(-0.7, 0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0, -0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET, precision=50, func=self.target_1_func, target_pts=[15])
        stage_1["target_2"] = cf.new_button(50, (0, 0, 255, 120), random.uniform(-0.7, 0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0, -0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET, precision=50, func=self.target_2_func, target_pts=[16])

        self.stages = [stage_0, stage_1]
        self.stage = 0

        self.components = self.stages[self.stage]

    def time_expire_func(self) -> None:
        self.stage = 0
        self.change_stage()
        if STOP_LOGGING in self.funcs:
            for func in self.funcs[STOP_LOGGING]:
                func()
    
    def target_1_func(self) -> None:
        self.stages[1]["target_1"].set_pos(random.uniform(-0.7,0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0,-0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET)
        pass

    def target_2_func(self) -> None:
        self.stages[1]["target_2"].set_pos(random.uniform(-0.7,0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0,-0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET)
        pass

    def start_button_func(self) -> None:
        if self.stage == 0:
            self.persist[TIMER].set_timer(10)
            self.persist[TIMER].start_timer()
            self.stage = self.stage + 1
            if NEW_LOG in self.funcs:
                for func in self.funcs[NEW_LOG]:
                    func()
            if START_LOGGING in self.funcs:
                for func in self.funcs[START_LOGGING]:
                    func()

    def handle_frame(self, **kwargs) -> None:
        super().handle_frame(**kwargs)
        self.change_stage()