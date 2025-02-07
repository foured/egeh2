from typing import Type, List, Any, TypeVar

from src.activities.rus_activities import *

PDT = TypeVar('T')

class ActivitiesHub():
    activities: List[Any] = []

    @staticmethod
    def setup():
        ActivitiesHub.activities.append(RussianNumber_4())
        ActivitiesHub.activities.append(RussianHTR())

    @staticmethod
    def get(type: Type[PDT]) -> PDT:
        for activity in ActivitiesHub.activities:
            if isinstance(activity, type):
                return activity
        return None
