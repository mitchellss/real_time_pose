
import threading
from playsound import playsound
from constants.constants import PATH
from feedback.feedback_device import FeedbackDevice


class ComputerSoundFeedback(FeedbackDevice):

    def __init__(self) -> None:
        super().__init__()

    def connect(self) -> None:
        return super().connect()

    def disconnect(self) -> None:
        return super().disconnect()

    def beep(self):
        threading.Thread(target=playsound, args=(PATH / "feedback/beep.mp3",), daemon=True).start()
