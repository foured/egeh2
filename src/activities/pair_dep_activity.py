import random

class PairDependendActivity():
    def __init__(self, path: str) -> None:
        with open(path, encoding='utf-8') as file:
            words = [ws for ws in [line.split() for line in file]]
            self.c_words = [ws[0] for ws in words]
            self.w_words = [ws[1] for ws in words]

    def get_random_pair(self) -> tuple[str, str]:
        ri = random.randint(0, len(self.c_words) - 1)
        return self.c_words[ri], self.w_words[ri]

    def is_word_correct(self, word: str) -> bool:
        return word in self.c_words
    
    def get_correct_words(self) -> str:
        res = ''
        for word in self.c_words:
            res += word + '\n'
        return res.strip()
    
    def get_correct_word(self, input: str) -> str:
        for i in range(len(self.c_words)):
            if self.c_words[i].lower()[0] > input.lower()[0]:
                break

            if self.c_words[i] == input or self.w_words[i] == input:
                return self.c_words[i]
            
        return 'unknown word'

    def get_word_id(self, input: str) -> int:
        li = input.lower()
        for i in range(len(self.c_words)):
            if self.c_words[i].lower()[0] > li[0]:
                break 

            if self.c_words[i].lower() == li:
                return i
        return -1

    def get_random_id(self) -> int:
        return random.randint(0, len(self.c_words) - 1)

    def get_pair(self, idx: int) -> tuple[str, str]:
        return self.c_words[idx], self.w_words[idx]

    def get_words_len(self) -> int:
        return len(self.c_words)

    def create_statistics_array(self) -> list[int]:
        return [0] * self.get_words_len()