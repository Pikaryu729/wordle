import random
import rich


def is_valid_guess(words: list[str], word:str) -> bool:
    """ returns True if valid guess, else false """
    if len(word) != 5:
        return False
    if word not in words:
        return False
    
class Game:
    def __init__(self, words_file: str = "words.txt", seed: int | None = None):
        self.words = self.load_words(words_file)
        if seed:
            self.generator = random.Random(seed)
        else:
            self.generator = random.Random() 
    
    @classmethod
    def load_words(self, words_file: str) -> list[str]:
        with open(words_file, "r") as file:
            words = file.readlines()
        return words

    def get_random_word(self):
        """ Gets random word from list of words"""
        return self.generator.choice(self.words)
