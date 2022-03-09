
from types import FunctionType
import numpy as np
from activities.activity import Activity
from activities.bread_crumb.bread_crumb import BreadCrumb
from activities.custom_activity_dynamic.custom_activity_dynamic import CustomActivityDynamic
from activities.game.game import Game
from activities.game_mk2.game_mk2 import GameMkII
from activities.haptic.haptic import Haptic
from activities.jumping_jacks.jumping_jacks import JumpingJacks
from activities.record_data.record_data import RecordData
from activities.shapes.shapes import Shapes
from activities.squat.squat import Squat
from activities.vector_haptic.vector_haptic import VectorHaptic


class ActivityFactory:

    def __init__(self, type: str) -> None:
        self.type = type
    
    def new_activity(self, body_point_array: np.array, ui: str, funcs: dict[str,list[FunctionType]], path: str) -> Activity:
        if self.type == "game":
            return Game(body_point_array, ui, funcs=funcs)
        elif self.type == "jumping_jacks":
            return JumpingJacks(body_point_array, ui, funcs=funcs)
        elif self.type == "squat":
            return Squat(body_point_array, ui, funcs=funcs)
        elif self.type == "bread_crumb":
            return BreadCrumb(body_point_array, ui, funcs=funcs, path=path)
        elif self.type == "custom_activity_dynamic":
            return CustomActivityDynamic(body_point_array, ui, funcs=funcs, path=path)
        elif self.type == "game_mk2":
            return GameMkII(body_point_array, ui, funcs=funcs, path=path)
        elif self.type == "haptic":
            return Haptic(body_point_array, ui, funcs=funcs, path=path)
        elif self.type == "shapes":
            return Shapes(body_point_array, ui, funcs=funcs, path=path)
        elif self.type == "vector_haptic":
            return VectorHaptic(body_point_array, ui, funcs=funcs, path=path)
        elif self.type == "record_data":
            return RecordData(body_point_array, ui, funcs=funcs, path=path)
        else:
            return None
