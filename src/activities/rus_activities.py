from src.activities.pair_dep_activity import PairDependendActivity
from src.activities.insert_val_activity import InsertValueActivity

class RussianNumber_4(PairDependendActivity):
    def __init__(self):
        super().__init__('res/rus_n4_2025.txt')

class RussianNumber_9(PairDependendActivity):
    def __init__(self):
        super().__init__('res/rus_n9.txt')

class RussianNumber_10(PairDependendActivity):
    def __init__(self):
        super().__init__('res/rus_n10.txt', '; ')
    
class RussianVocabulary(PairDependendActivity):
    def __init__(self):
        super().__init__('res/rus_vcblr.txt')

class RussianVerbSuffix(InsertValueActivity):
    def __init__(self):
        super().__init__('res/vrb_sfx.txt')