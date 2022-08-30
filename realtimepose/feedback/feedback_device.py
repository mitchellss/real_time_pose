from typing_extensions import Protocol


class FeedbackDevice(Protocol):

    def __init__(self) -> None:
        pass

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass