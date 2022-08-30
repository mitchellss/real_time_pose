
from ui.components.button_component import ButtonComponent
from ui.components.hand_bubble_component import HandBubbleComponent
from ui.components.live_score_component import LiveScoreComponent
from ui.components.skeleton_component import SkeletonComponent
from ui.components.text_component import TextComponent
from ui.components.timer_component import TimerComponent
from ui.pygame.pygame_button import PyGameButton
from ui.pygame.pygame_hand_bubble import PyGameHandBubble
from ui.pygame.pygame_live_score import PyGameLiveScore
from ui.pygame.pygame_skeleton import PyGameSkeleton
from ui.pygame.pygame_text import PyGameText
from ui.pygame.pygame_timer import PyGameTimer
from ui.pyqtgraph.pyqtgraph_button import PyQtGraphButton
from ui.pyqtgraph.pyqtgraph_hand_bubble import PyQtGraphHandBubble
from ui.pyqtgraph.pyqtgraph_live_score import PyQtGraphLiveScore
from ui.pyqtgraph.pyqtgraph_skeleton import PyQtGraphSkeleton
from ui.pyqtgraph.pyqtgraph_text import PyQtGraphText
from ui.pyqtgraph.pyqtgraph_timer import PyQtGraphTimer


class ComponentFactory():

    def __init__(self, ui: str) -> None:
        self.ui = ui

    def new_button(self, size: int, color: tuple[int, int, int, int], x_pos: float,
                 y_pos: float, precision: float = 0, **kwargs) -> ButtonComponent:
        if self.ui == "pyqtgraph":
            return PyQtGraphButton(size, color, x_pos, y_pos, precision, **kwargs)
        elif self.ui == "pygame":
            return PyGameButton(size, color, x_pos, y_pos, precision, **kwargs)

    def new_hand_bubble(self, x_pos: float, y_pos: float, target: int, size: int, color: tuple[int, int, int, int]) -> HandBubbleComponent:
        if self.ui == "pyqtgraph":
            return PyQtGraphHandBubble(x_pos, y_pos, target, size, color)
        elif self.ui == "pygame":
            return PyGameHandBubble(x_pos, y_pos, target, size, color)

    def new_live_score(self, x_pos: float, y_pos: float, **kwargs) -> LiveScoreComponent:
        if self.ui == "pyqtgraph":
            return PyQtGraphLiveScore(x_pos, y_pos, **kwargs)
        elif self.ui == "pygame":
            return PyGameLiveScore(x_pos, y_pos, **kwargs)

    def new_skeleton(self, skeleton_array) -> SkeletonComponent:
        if self.ui == "pyqtgraph":
            return PyQtGraphSkeleton(skeleton_array)
        elif self.ui == "pygame":
            return PyGameSkeleton(skeleton_array)

    def new_text(self, x_pos: float, y_pos: float, text: str, **kwargs) -> TextComponent:
        if self.ui == "pyqtgraph":
            return PyQtGraphText(x_pos, y_pos, text, **kwargs)
        elif self.ui == "pygame":
            return PyGameText(x_pos, y_pos, text, **kwargs)

    def new_timer(self, x_pos: float, y_pos: float, **kwargs) -> TimerComponent:
        if self.ui == "pyqtgraph":
            return PyQtGraphTimer(x_pos, y_pos, **kwargs)
        elif self.ui == "pygame":
            return PyGameTimer(x_pos, y_pos, **kwargs)
