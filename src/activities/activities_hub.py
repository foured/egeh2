from typing import Type, List, Any, TypeVar

from src.activities.rus_num_4 import RussianNumber_4

PDT = TypeVar('T')

class ActivitiesHub():
    activities: List[Any] = []

    @staticmethod
    def setup():
        ActivitiesHub.activities.append(RussianNumber_4())

    @staticmethod
    def get(type: Type[PDT]) -> PDT:
        for activity in ActivitiesHub.activities:
            if isinstance(activity, type):
                return activity
        return None
