from activities.activity import Activity
from ui.pygame.pygame_button import PyGameButton
from ui.pygame.pygame_hand_bubble import PyGameHandBubble
from ui.pygame.pygame_live_score import PyGameLiveScore
from ui.pygame.pygame_skeleton import PyGameSkeleton
from ui.pygame.pygame_text import PyGameText
from ui.pygame.pygame_timer import PyGameTimer
from constants.constants import *
import sys
import pandas as pd
from better_profanity import profanity

from utils.utils import *


class GameMkII(Activity):
    """Second version of the original game. Buttons move around and players have
    to keep their hands in them as long as possible to earn the highest score.

    Args:
        Activity ([type]): Abstract activity object
    """

    STARTING_STAGE = 0
    PLAY_STAGE = 1
    NAME_STAGE = 2

    def __init__(self, body_point_array, **kwargs) -> None:

        # Initialize persistant component dict (Never dissapear reguardless of active stage)
        self.persist = {}
        self.persist[SKELETON] = PyGameSkeleton(body_point_array)
        self.persist[TIMER] = PyGameTimer(WINDOW_WIDTH-250, 60, size=50, func=self.time_expire_func)
        self.persist[LIVE_SCORE] = PyGameLiveScore(WINDOW_WIDTH-250, 110, size=50)

        # Initialize dict for stage 0 
        stage_0 = {}
        stage_0[START_TARGET] = PyGameButton(50, (0, 255, 0, 120), 
                                            0*PIXEL_SCALE+PIXEL_X_OFFSET, 
                                            -0.6*PIXEL_SCALE+PIXEL_Y_OFFSET, 
                                            precision=50, func=self.start_button_func, target_pts=[16, 15])

        # Initialize path variable if specified in kwargs
        if PATH_ARG in kwargs:
            self.file_path = kwargs[PATH_ARG]

        # Initializes a dict of functions where various capabilities can be passed
        # i.e (Start logging, stop logging, etc.)
        if FUNCS in kwargs:
            self.funcs = kwargs[FUNCS]
        else:
            self.funcs = {}

        # Attempts to read point data from specified CSV, otherwise exits
        try:
            points_data = pd.read_csv(self.file_path)
        except:
            print("Cannot find csv file specified")
            sys.exit(1)

        # Set data for each point (based on https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png)
        self.lh_x_data = points_data["x15"]
        self.lh_y_data = points_data["y15"]

        self.rh_x_data = points_data["x16"]
        self.rh_y_data = points_data["y16"]

        self.ll_x_data = points_data["x27"]
        self.ll_y_data = points_data["y27"]

        self.rl_x_data = points_data["x28"]
        self.rl_y_data = points_data["y28"]
        
        # Index tracks point in the file for a specific group of buttons/points
        self.index = 0

        self.letter_change_delay = 0

        self.letter_index = [0,0,0,0]

        # Initialize stage 1 dict. This contains all the buttons
        stage_1 = {}
        stage_1[TARGET_0] = PyGameButton(50, (255, 0, 0, 60),
                                              bp2p_x(float(self.lh_x_data[self.index])), 
                                              bp2p_y(float(self.lh_y_data[self.index])),
                                              func=self.target_1_func, target_pts=[15], precision=50)

        stage_1[TARGET_1] = PyGameButton(50, (0, 0, 255, 60),
                                              bp2p_x(float(self.rh_x_data[self.index])), 
                                              bp2p_y(float(self.rh_y_data[self.index])),
                                              func=self.target_2_func, target_pts=[16], precision=50)

        stage_1[TARGET_2] = PyGameButton(50, (255, 255, 0, 60),
                                              bp2p_x(float(self.ll_x_data[self.index])), 
                                              bp2p_y(float(self.ll_y_data[self.index])),
                                              func=self.target_3_func, target_pts=[27], precision=50)

        stage_1[TARGET_3] = PyGameButton(50, (0, 255, 255, 60),
                                              bp2p_x(float(self.rl_x_data[self.index])), 
                                              bp2p_y(float(self.rl_y_data[self.index])),
                                              func=self.target_4_func, target_pts=[28], precision=50)

        stage_1["bubble_1"] = PyGameHandBubble(0, 0, 15, 30, (255, 0, 0, 120))
        stage_1["bubble_2"] = PyGameHandBubble(0, 0, 16, 30, (0, 0, 255, 120))
        stage_1["bubble_3"] = PyGameHandBubble(0, 0, 27, 30, (255, 255, 0, 120))
        stage_1["bubble_4"] = PyGameHandBubble(0, 0, 28, 30, (0, 255, 255, 120))

        horz_starting_pt = -0.4
        spacing = 0.25
        height = 240
        initial_offset = 25
        first_offset = 55
        second_offset = 165
        spacing = 10

        letter_centering_vert = -70

        stage_2 = {}
        stage_2["bubble_1"] = PyGameHandBubble(0, 0, 15, 30, (255, 0, 0, 120))
        stage_2["bubble_2"] = PyGameHandBubble(0, 0, 16, 30, (0, 0, 255, 120))
        stage_2[NAME_TARGET_0 + UP] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset - second_offset, 
                                                        height, 
                                                        func=lambda:self.change_letter(0,1), target_pts=[15], precision=50)
        stage_2[NAME_TARGET_0 + DOWN] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset - second_offset, 
                                                          height, 
                                                          func=lambda:self.change_letter(0,-1), target_pts=[16], precision=50)
        stage_2[NAME_TARGET_1 + UP] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset - first_offset, 
                                                        height, 
                                                        func=lambda:self.change_letter(1,1), target_pts=[15], precision=50)
        stage_2[NAME_TARGET_1 + DOWN] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset - first_offset, 
                                                          height, 
                                                          func=lambda:self.change_letter(1,-1), target_pts=[16], precision=50)
        stage_2[NAME_TARGET_2 + UP] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset + first_offset, 
                                                        height, 
                                                        func=lambda:self.change_letter(2,1), target_pts=[15], precision=50)
        stage_2[NAME_TARGET_2 + DOWN] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset + first_offset, 
                                                          height, 
                                                          func=lambda:self.change_letter(2,-1), target_pts=[16], precision=50)
        stage_2[NAME_TARGET_3 + UP] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset + second_offset, 
                                                        height, 
                                                        func=lambda:self.change_letter(3,1), target_pts=[15], precision=50)
        stage_2[NAME_TARGET_3 + DOWN] = PyGameButton(50, (0, 255, 0, 60),
                                                        WINDOW_WIDTH/2 - initial_offset + second_offset, 
                                                          height, 
                                                          func=lambda:self.change_letter(3,-1), target_pts=[16], precision=50)
        stage_2["name_label_0"] = PyGameText(
            WINDOW_WIDTH/2 - initial_offset - second_offset - 15, height+letter_centering_vert - 35, text="A", size=50)
        stage_2["name_label_1"] = PyGameText(
            WINDOW_WIDTH/2 - initial_offset - first_offset - 15, height+letter_centering_vert - 35, text="A", size=50)
        stage_2["name_label_2"] = PyGameText(
            WINDOW_WIDTH/2 - initial_offset + first_offset - 15, height+letter_centering_vert - 35, text="A", size=50)
        stage_2["name_label_3"] = PyGameText(
            WINDOW_WIDTH/2 - initial_offset + second_offset - 15, height+letter_centering_vert - 35, text="A", size=50)
        stage_2["submit_button"] = PyGameButton(50, (0, 255, 0, 120),
                                                     WINDOW_WIDTH-250, WINDOW_HEIGHT/2-100, func=self.submit_score_func, target_pts=[15], precision=50)
        stage_2["submit_label"] = PyGameText(
            WINDOW_WIDTH-250-45, WINDOW_HEIGHT/2-190, text="Submit")
        stage_2["letter_instructions_1"] = PyGameText(
            20, 0, text="Enter your name and submit your score!", size=50, font="Sans")
        # stage_2["letter_instructions_2"] = PyGameText(
        #     20, WINDOW_HEIGHT/2+30-300, text="Red goes forwards", color=(255,0,0))
        # stage_2["letter_instructions_3"] = PyGameText(
        #     20, WINDOW_HEIGHT/2+60-300, text="Blue goes back", color=(50,50,255))


        # List of stages to swap between and what stage to start at
        self.stages = [stage_0, stage_1, stage_2]
        self.stage = 0

        # # Use this to start at stage 1
        # self.stage = 1
        # self.persist[TIMER].set_timer(1)

        # Set the active components to the dict of the initial stage
        self.components = self.stages[self.stage]

    def change_letter(self, letter_num, amount):
        self.letter_change_delay += 1
        if self.letter_change_delay % 5 == 0:
            self.letter_index[letter_num] = (self.letter_index[letter_num] + amount) % len(LETTER_SELECT)
            for i in range(0,4): 
                self.stages[self.NAME_STAGE][f"name_label_{i}"].set_text(LETTER_SELECT[self.letter_index[i]])
        self.persist[TIMER].set_timer(20)


    def submit_score_func(self):
        self.stage = 0
        name = f"{LETTER_SELECT[self.letter_index[0]]}{LETTER_SELECT[self.letter_index[1]]}{LETTER_SELECT[self.letter_index[2]]}{LETTER_SELECT[self.letter_index[3]]}"
        if not profanity.contains_profanity(name):
            file = open(PATH / "leaderboard.txt", "a")
            file.write(f"{name},{self.persist[LIVE_SCORE].get_score()}\n")
            file.close()
            self.persist[LIVE_SCORE].set_score(0)

    def time_expire_func(self) -> None:
        if self.stage == 1:
            self.stage = 2
            self.index = 0
            if STOP_LOGGING in self.funcs:
                for func in self.funcs[STOP_LOGGING]:
                    func()
            self.persist[TIMER].set_timer(20)
            self.persist[TIMER].hide()
        elif self.stage == 2:
            self.submit_score_func()
    
    def target_1_func(self) -> None:
        self.stages[self.PLAY_STAGE][TARGET_0].clicked = True
        self.stages[self.PLAY_STAGE][TARGET_0].change_color((255, 0, 0, 120))
        self.persist[LIVE_SCORE].add_score(0.1)

    def target_2_func(self) -> None:
        self.stages[self.PLAY_STAGE][TARGET_1].clicked = True
        self.stages[self.PLAY_STAGE][TARGET_1].change_color((0, 0, 255, 120))
        self.persist[LIVE_SCORE].add_score(0.1)

    def target_3_func(self) -> None:
        self.stages[self.PLAY_STAGE][TARGET_2].clicked = True
        self.stages[self.PLAY_STAGE][TARGET_2].change_color((255, 255, 0, 120))
        self.persist[LIVE_SCORE].add_score(0.1)

    def target_4_func(self) -> None:
        self.stages[self.PLAY_STAGE][TARGET_3].clicked = True
        self.stages[self.PLAY_STAGE][TARGET_3].change_color((0, 255, 255, 120))
        self.persist[LIVE_SCORE].add_score(0.1)

    def start_button_func(self) -> None:
        """
        Defines what should happen when the start button is pressed. In this
        case, it sets the timer to 100, increments the stage, creates new logs,
        starts the logs, and activates the stage change.
        """
        if self.stage == 0:
            self.persist[TIMER].show()
            self.persist[TIMER].set_timer(10)
            self.stage = self.stage + 1
            if NEW_LOG in self.funcs:
                for func in self.funcs[NEW_LOG]:
                    func()
            if START_LOGGING in self.funcs:
                for func in self.funcs[START_LOGGING]:
                    func()

    def handle_frame(self, **kwargs) -> None:
        """
        Defines what should happen at the end of a frame. In this case, it
        resets all the buttons to no longer be clicked.
        """
        super().handle_frame(**kwargs)

        if self.stage == self.PLAY_STAGE:
            if not self.stages[self.PLAY_STAGE][TARGET_0].clicked:
                self.stages[self.PLAY_STAGE][TARGET_0].change_color((120, 0, 0, 60))
            if not self.stages[self.PLAY_STAGE][TARGET_1].clicked:
                self.stages[self.PLAY_STAGE][TARGET_1].change_color((0, 0, 120, 60))
            if not self.stages[self.PLAY_STAGE][TARGET_2].clicked:
                self.stages[self.PLAY_STAGE][TARGET_2].change_color((120, 120, 0, 60))
            if not self.stages[self.PLAY_STAGE][TARGET_3].clicked:
                self.stages[self.PLAY_STAGE][TARGET_3].change_color((0, 120, 120, 60))
            
            self.stages[self.PLAY_STAGE][TARGET_0].clicked = False
            self.stages[self.PLAY_STAGE][TARGET_1].clicked = False
            self.stages[self.PLAY_STAGE][TARGET_2].clicked = False
            self.stages[self.PLAY_STAGE][TARGET_3].clicked = False

            self.index += 1
            self.stages[self.PLAY_STAGE][TARGET_0].set_pos(float(self.lh_x_data[self.index])*PIXEL_SCALE+PIXEL_X_OFFSET, float(self.lh_y_data[self.index])*PIXEL_SCALE+PIXEL_Y_OFFSET)
            self.stages[self.PLAY_STAGE][TARGET_1].set_pos(float(self.rh_x_data[self.index])*PIXEL_SCALE+PIXEL_X_OFFSET, float(self.rh_y_data[self.index])*PIXEL_SCALE+PIXEL_Y_OFFSET)
            self.stages[self.PLAY_STAGE][TARGET_2].set_pos(float(self.ll_x_data[self.index])*PIXEL_SCALE+PIXEL_X_OFFSET, float(self.ll_y_data[self.index])*PIXEL_SCALE+PIXEL_Y_OFFSET)
            self.stages[self.PLAY_STAGE][TARGET_3].set_pos(float(self.rl_x_data[self.index])*PIXEL_SCALE+PIXEL_X_OFFSET, float(self.rl_y_data[self.index])*PIXEL_SCALE+PIXEL_Y_OFFSET)

        self.change_stage()
