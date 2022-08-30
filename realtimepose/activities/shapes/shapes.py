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


class Shapes(Activity):
    """Different shapes

    Args:
        Activity ([type]): Abstract activity object
    """

    STARTING_STAGE = 0
    PLAY_STAGE = 1
    NAME_STAGE = 2

    def __init__(self, body_point_array, ui, **kwargs) -> None:
        super().__init__(body_point_array, ui, **kwargs)
        
        # Initialize persistant component dict (Never dissapear reguardless of active stage)
        self.persist = {}
        self.persist[SKELETON] = PyGameSkeleton(body_point_array)
        self.persist[TIMER] = PyGameTimer(WINDOW_WIDTH-250, 60, size=50, func=self.time_expire_func)
        self.persist[LIVE_SCORE] = PyGameLiveScore(WINDOW_WIDTH-250, 110, size=50)

        # Initialize dict for stage 0 
        stage_0 = {}
        stage_0[START_TARGET] = PyGameButton(50, (0, 0, 255, 120), 
                                            0*PIXEL_SCALE+PIXEL_X_OFFSET, 
                                            -0.6*PIXEL_SCALE+PIXEL_Y_OFFSET-100, 
                                            precision=50, func=self.start_button_func, target_pts=[16])
        stage_0["bubble_0"] = PyGameHandBubble(0, 0, 16, 30, (0, 0, 255, 120))

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
        self.speed = 1
        self.hit_miss = 0

        self.letter_change_delay = 0

        self.letter_index = [0,0,0,0]

        # Initialize stage 1 dict. This contains all the buttons
        stage_1 = {}
        stage_1[TARGET_0] = PyGameButton(50, (255, 0, 0, 60),
                                              bp2p_x(float(self.lh_x_data[self.index])), 
                                              bp2p_y(float(self.lh_y_data[self.index])),
                                              func=self.target_1_func, target_pts=[15], precision=50)

        stage_1["bubble_1"] = PyGameHandBubble(0, 0, 15, 30, (255, 0, 0, 120))

        # List of stages to swap between and what stage to start at
        self.stages = [stage_0, stage_1]
        self.stage = 0

        # # Use this to start at stage 1
        # self.stage = 1
        # self.persist[TIMER].set_timer(30)

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
            
            with open('leaderboard.txt') as f:
                lines = f.read().splitlines()
                for i in range(0,len(lines)):
                    lines[i] = lines[i].split(",")

                def myFunc(e):
                    return float(e[1])
                
                lines.sort(key=myFunc, reverse=True)

                self.print_scoreboard(lines)
    
    def print_scoreboard(self, lines):
        print("\n" * 50)
        for i in range(0,10):
            try:
                print(f"{i+1}. {lines[i][0]} - {lines[i][1][0:5]}")
            except:
                continue


    def time_expire_func(self) -> None:
        if self.stage == 1:
            self.stage = 0
            self.index = 0
            if CLOSE in self.funcs:
                for func in self.funcs[CLOSE]:
                    func()
            self.persist[TIMER].set_timer(20)
            self.persist[TIMER].hide()
    
    def target_1_func(self) -> None:
        self.stages[self.PLAY_STAGE][TARGET_0].clicked = True
        self.stages[self.PLAY_STAGE][TARGET_0].change_color((255, 0, 0, 120))
        self.persist[LIVE_SCORE].add_score(0.1)

    def start_button_func(self) -> None:
        """
        Defines what should happen when the start button is pressed. In this
        case, it sets the timer to 100, increments the stage, creates new logs,
        starts the logs, and activates the stage change.
        """
        if self.stage == 0:
            self.persist[TIMER].show()
            self.persist[TIMER].set_timer(30)
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
                self.hit_miss -= 1
            else:
                self.hit_miss += 1
            
            if self.hit_miss < 0 and self.speed > 0.7:
                self.speed -= 0.01
                # self.stages[self.PLAY_STAGE][TARGET_0].precision += 0.1
                # self.stages[self.PLAY_STAGE][TARGET_1].precision += 0.1
                # self.stages[self.PLAY_STAGE][TARGET_2].precision += 0.1
                # self.stages[self.PLAY_STAGE][TARGET_3].precision += 0.1
            
            if self.hit_miss > 0 and self.speed < 1:
                self.speed += 0.01
                # self.stages[self.PLAY_STAGE][TARGET_0].precision -= 0.1
                # self.stages[self.PLAY_STAGE][TARGET_1].precision -= 0.1
                # self.stages[self.PLAY_STAGE][TARGET_2].precision -= 0.1
                # self.stages[self.PLAY_STAGE][TARGET_3].precision -= 0.1

            if self.hit_miss > 150:
                self.hit_miss = 150

            if self.hit_miss < -150:
                self.hit_miss = -150

            self.stages[self.PLAY_STAGE][TARGET_0].clicked = False
            self.index += self.speed

            self.stages[self.PLAY_STAGE][TARGET_0].set_pos(float(self.lh_x_data[round(self.index)])*PIXEL_SCALE+PIXEL_X_OFFSET, float(self.lh_y_data[round(self.index)])*PIXEL_SCALE+PIXEL_Y_OFFSET)



        self.change_stage()
