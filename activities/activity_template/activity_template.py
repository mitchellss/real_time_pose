
from activities.activity import Activity
from constants.constants import *
from ui.components.component_factory import ComponentFactory
from utils.utils import *


class ActivityTemplate(Activity):

    def __init__(self, body_point_array, ui, **kwargs) -> None:
        # Need to call the parent class's init to instantiate the needed global variables
        super().__init__(body_point_array, ui, **kwargs)

        # Need to create a compoonent factory to produce all the buttons/skeleton/timer/score
        # This way, the GUI can be switched out easily
        cf = ComponentFactory(self.ui)

        # Persist is everything that is ALWAYS on the screen no matter what
        # This usually includes the skeleton (the thing dots and lines that replicate the person),
        # the timer, and the score (if it is included)
        self.persist = {}
        self.persist[SKELETON] = cf.new_skeleton(body_point_array)
        self.persist[TIMER] = cf.new_timer(300, 50, func=self.time_expire_func)

        # A "stage" is a group of components that all get shown at the same time. Every frame the 
        # program checks to make sure that only the items that are in the current stage are shown.
        # This does not affect "persist" components, which are always shown no matter what. (unless they are specifically hidden)
        stage_0 = {}

        # How to add a button to a specific stage. This button will now disappear if the stage is changed. To reference this button later on,
        # use self.stages[X]["{COMPONENT NAME}"]
        # "func" points to the action that you want the button to do if it is "clicked"
        # "target_pts" are the points on the skeleton that can "click" the button
        stage_0["start_target"] = cf.new_button(50, (0, 255, 0, 120), bp2p_x(0), bp2p_y(-0.6), precision=50, func=self.start_button_func, target_pts=[16, 15])

        stage_1 = {}
        # Add more stages as needed
        #stage_1["target_1"] = cf.new_button(50, (255, 0, 0, 120), random.uniform(-0.7, 0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0, -0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET, precision=50, func=self.target_1_func, target_pts=[15])
        #stage_1["target_2"] = cf.new_button(50, (0, 0, 255, 120), random.uniform(-0.7, 0.7)*PIXEL_SCALE+PIXEL_X_OFFSET, random.uniform(0.0, -0.8)*PIXEL_SCALE+PIXEL_Y_OFFSET, precision=50, func=self.target_2_func, target_pts=[16])

        # VERY IMPORTANT: Add your stages to a list and set the self.stage variable to the stage you want to start on. This is how
        # the program knows what components to render at any given time.
        self.stages = [stage_0, stage_1]
        self.stage = 0

        self.components = self.stages[self.stage]

    # Function that executes when the timer hits zero. Usually this means that
    # the stage needs to change, the score needs to be reset, logging needs to stop, etc.
    def time_expire_func(self) -> None:
        self.stage = 0

        # This code iterates through all the active loggers and makes sure they stop. 
        # Loggers are setup in the "main.py" file
        if STOP_LOGGING in self.funcs:
            for func in self.funcs[STOP_LOGGING]:
                func()
    
    # Use functions like this to manipulate components when
    # buttons are pressed. For each button added, you'll likely
    # want to implement a new function defining what the button
    # should do.
    def start_button_func(self) -> None:
        # If you wanted to start a timer with 10 seconds:
        #
        # self.persist[TIMER].set_timer(10)
        # self.persist[TIMER].start_timer()
        # self.stage = self.stage + 1

        # If you want to create new log files and start logging:
        #
        # if NEW_LOG in self.funcs:
        #     for func in self.funcs[NEW_LOG]:
        #         func()
        # if START_LOGGING in self.funcs:
        #     for func in self.funcs[START_LOGGING]:
        #         func()

        pass

    # VERY IMPORTANT: The "handle_frame" function runs on every frame
    # in order for buttons and other components to work properly you need
    # to make sure the parent class's method is called and the stage is changed.
    def handle_frame(self, **kwargs) -> None:
        super().handle_frame(**kwargs)
        self.change_stage()