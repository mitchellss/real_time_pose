
from ..ui import GUI
from .. import frame_input
from ..activities.activity import Activity
from ..activities.scene import Scene
from ..data_logging import Logger


BLAZEPOSE = 0

def new_activity(input: frame_input, gui: GUI, backend: int) -> Activity:
    return Activity()

def new_scene() -> Scene:
    return Scene()

def add_logger(logger: Logger):
    return Logger()