import random

from src.activities.pair_dep_activity import PairDependendActivity

class RussianNumber_4(PairDependendActivity):
    def __init__(self):
        super().__init__('res/rus_n4_2025.txt')

class RussianHTR(PairDependendActivity):
    def __init__(self):
        super().__init__('res/rus_htr.txt', False)