import re
import random

from src.activities.activity_base import ActivityBase

class InsertValueActivity(ActivityBase):
    class InsertedItem():
        def __init__(self, line: str, id: int) -> None:
            self.id = id
            parts = re.split(r'\s*\[\s*|\s*\]\s*', line.strip())
    
            self.word = parts[0]
            self.items = [item.strip() for item in parts[1:-1] if item.strip()]
            
            if self.items:
                self.items = [item for sublist in [item.split(',') for item in self.items] for item in sublist]
                self.items = [item.strip() for item in self.items if item.strip()]
            
        def check(self, val: str):
            return val.lower() == self.items[0].lower()
        
        def get_correct(self) -> str:
            return self.word.replace('...', self.items[0])

    def __init__(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.items = [InsertValueActivity.InsertedItem(lines[i], i) for i in range(len(lines))]

    def get_random_item(self) -> InsertedItem:
        return random.choice(self.items)
    
    def create_statistics_array(self) -> list[int]:
        return [0] * len(self.items)
    
    def get_random_id(self) -> int:
        return random.choice(range(len(self.items)))
    
    def get_item(self, idx: int) -> InsertedItem:
        return self.items[idx]
    
    def get_answer(self, idx: int) -> str:
        i = self.items[idx]
        w = i.word
        return w.replace('...', i.items[0])
    
    def get_all_words(self) -> str:
        s = ''
        for i in self.items:
            s += i.get_correct() + '\n'
        return s.strip()