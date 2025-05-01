from abc import *

class ActivityBase():
    @abstractmethod
    def get_answer(self, idx: int) -> str:
        pass