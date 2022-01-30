import pathlib
from threading import Timer

PATH = pathlib.Path(__file__).parent.parent.resolve()
TARGET_0 = "target_0"
TARGET_1 = "target_1"
TARGET_2 = "target_2"
TARGET_3 = "target_3"

NAME_TARGET_0 = "name_target_0"
NAME_TARGET_1 = "name_target_1"
NAME_TARGET_2 = "name_target_2"
NAME_TARGET_3 = "name_target_3"

START_TARGET = "start_target"

LETTER_SELECT = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                    'O','P','Q','R','S','T','U','V','W','X','Y','Z']

SKELETON = "skeleton"
TIMER = "timer"
LIVE_SCORE = "live_score"

UP = "_up"
DOWN = "_down"

STOP_LOGGING = "stop_logging"
START_LOGGING = "start_logging"
NEW_LOG = "new_log"

PATH_ARG = "path"
FUNCS = "funcs"