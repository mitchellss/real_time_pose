import pathlib

PATH = pathlib.Path(__file__).parent.parent.resolve()
TARGET_0: str = "target_0"
TARGET_1: str = "target_1"
TARGET_2: str = "target_2"
TARGET_3: str = "target_3"

NAME_TARGET_0: str = "name_target_0"
NAME_TARGET_1: str = "name_target_1"
NAME_TARGET_2: str = "name_target_2"
NAME_TARGET_3: str = "name_target_3"

START_TARGET: str = "start_target"

LETTER_SELECT: list[str] = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                    'O','P','Q','R','S','T','U','V','W','X','Y','Z']

SKELETON: str = "skeleton"
TIMER: str = "timer"
LIVE_SCORE: str = "live_score"

UP: str = "_up"
DOWN: str = "_down"

STOP_LOGGING: str = "stop_logging"
START_LOGGING: str = "start_logging"
NEW_LOG: str = "new_log"

PATH_ARG: str = "path"
FUNCS: str = "funcs"

PIXEL_SCALE: int = 500
PIXEL_X_OFFSET: int = 450
PIXEL_Y_OFFSET: int = 500

WINDOW_WIDTH: int = 1920//2
WINDOW_HEIGHT: int = 1000
