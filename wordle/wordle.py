import random
from rich.console import Console
from rich.prompt import Prompt


class Wordle:

    def __init__(self, words_file: str = "words.txt", seed: int | None = None):
        self.num_guesses = 0
        self.max_guesses = 6
        self.console = Console()
        self.allowed_words = self.load_words(words_file)
        if seed:
            self.generator = random.Random(seed)
        else:
            self.generator = random.Random()
        self.secret_word = self.get_random_word()
        self.has_won = False
        self.prev_guesses = []

    def load_words(self, words_file: str) -> list[str]:
        with open(words_file, "r") as file:
            words = [line.strip() for line in file]
        return words

    def get_random_word(self):
        """Gets random word from list of words"""
        return self.generator.choice(self.allowed_words)

    def is_valid_guess(self, word: str) -> bool:
        """returns True if valid guess, else false"""
        if word not in self.allowed_words:
            return False
        return True

    def check_guess(self, word: str) -> tuple[int]:
        """
        output list of numbers where:
        0 - character is not in word.
        1 - character is in word but at wrong possition.
        2 - character is in word, at right position
        """
        word_counts = {}
        out = [0] * len(self.secret_word)

        for char in self.secret_word:
            word_counts[char] = word_counts.get(char, 0) + 1

        for i, char in enumerate(word):
            if char == self.secret_word[i] and word_counts[char] > 0:
                word_counts[char] -= 1
                out[i] = 2

        for i, char in enumerate(word):
            if out[i] != 2 and char in self.secret_word and word_counts[char] > 0:
                word_counts[char] -= 1
                out[i] = 1

        return tuple(out)

    def get_guess(self) -> str:
        while True:
            guess = Prompt.ask("Enter a Guess")
            if self.is_valid_guess(guess):
                self.num_guesses += 1
                break
            self.console.print("[red]Invalid Guess. Please enter a valid 5 letter word")
        self.prev_guesses.append(guess)
        return guess

    def print_guess(self, guess):
        letter_statuses: list[int] = self.check_guess(guess)
        to_print = ""
        for status, letter in zip(letter_statuses, guess.upper()):
            if status == 0:
                to_print += f"[white on bright_black]{letter}[/] "
            elif status == 1:
                to_print += f"[white on bright_yellow]{letter}[/] "
            else:
                to_print += f"[white on bright_green]{letter}[/] "
        self.console.print(to_print)

    def print_prev_guesses(self):
        self.console.print("Previous: ")
        for guess in self.prev_guesses:
            self.print_guess(guess)

    def run(self):
        while self.num_guesses < self.max_guesses:
            self.print_prev_guesses()
            guess = self.get_guess()
            if guess == self.secret_word:
                self.has_won = True
                break
            self.print_guess(guess)
        self.game_over()

    def game_over(self):
        if self.has_won:
            print(f"You guess the word! {self.secret_word.upper()}")
        else:
            print(f"The word was: {self.secret_word}. Better luck next time!")
