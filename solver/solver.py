import math
from collections import defaultdict
from wordle.wordle import Wordle
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

BASE_DIR = Path(__file__).resolve().parent.parent


class Solver:
    def __init__(self, wordle: Wordle):
        self.wordle = wordle
        self.allowed_words = (
            wordle.allowed_words.copy()
        )  # Make a copy to avoid modifying original
        self.num_guesses = 0
        self.console = Console()

    def check_guess(self, guess: str, answer: str) -> tuple[int]:
        """
        output list of numbers where:
        0 - character is not in word.
        1 - character is in word but at wrong position.
        2 - character is in word, at right position
        """
        word_counts = {}
        out = [0] * len(guess)

        # Count characters in answer
        for char in answer:
            word_counts[char] = word_counts.get(char, 0) + 1

        # First pass: mark exact matches
        for i, char in enumerate(guess):
            if char == answer[i] and word_counts[char] > 0:
                word_counts[char] -= 1
                out[i] = 2

        # Second pass: mark characters in wrong position
        for i, char in enumerate(guess):
            if out[i] != 2 and char in answer and word_counts[char] > 0:
                word_counts[char] -= 1
                out[i] = 1

        return tuple(out)

    def get_guess_entropy(self, guess: str) -> float:
        """Calculate entropy for a given guess against current allowed words"""
        if not self.allowed_words:
            return 0.0

        pattern_counts = defaultdict(int)
        for word in self.allowed_words:
            pattern = self.check_guess(guess, word)
            pattern_counts[pattern] += 1

        entropy = 0.0
        total_words = len(self.allowed_words)
        for count in pattern_counts.values():
            if count > 0:  # Avoid log(0)
                probability = count / total_words
                entropy -= probability * math.log2(probability)

        return entropy

    def filter_words_by_response(self, guess: str, response: tuple) -> list[str]:
        """
        Filter word list to only include words that would give the specified response to the guess.
        """
        return [
            word
            for word in self.allowed_words
            if self.check_guess(guess, word) == response
        ]

    def get_letter_stauses(self, guess):
        return self.check_guess(guess, self.wordle.secret_word)

    def get_new_word_list(self, guess: str, letter_statuses: tuple[int]) -> list[str]:
        """Update word list based on the response to the current guess"""
        return self.filter_words_by_response(guess, letter_statuses)

    def get_best_guess(self) -> str:
        """Get the guess with the highest entropy from current allowed words"""
        if not self.allowed_words:
            return None

        entropy_table = {
            guess: self.get_guess_entropy(guess) for guess in self.allowed_words
        }
        return max(entropy_table, key=entropy_table.get)

    def get_valid_input(self) -> tuple[int]:
        while True:
            response = Prompt.ask(
                "Enter list of numbers: 0 - grey, 1 - yellow, 2 - green"
            )
            try:
                letter_statuses = [int(x) for x in response]
                if len(letter_statuses) != 5:
                    raise ValueError("You must enter exactly 5 digits")
                if not all(x in (0, 1, 2) for x in letter_statuses):
                    raise ValueError("Each must be between 0, 1, or 2")
                return tuple(letter_statuses)
            except ValueError as e:
                self.console.print(f"[red]Error:[/red] {e}")

    def user_solve(self):
        guess = "tares"  # starting guess
        letter_statuses = None
        guess_num = 1
        for i in range(self.wordle.max_guesses):
            self.console.print(f"Guess Number {guess_num}")
            self.console.print(f"Starting Guess: {guess}" if guess_num == 1 else f"Best Guess: {guess}")
            letter_statuses = self.get_valid_input()
            if letter_statuses == (2, 2, 2, 2, 2):
                break
            self.allowed_words = self.get_new_word_list(guess, letter_statuses)
            guess = self.get_best_guess()

            guess_num += 1
        print(f"Found Answer: {guess} in {guess_num} tries")

    def solve(self) -> str:
        """Solve the Wordle puzzle and return the solution"""
        guess = "tares"  # Starting guess

        while guess != self.wordle.secret_word:
            print(f"Guess {self.num_guesses + 1}: {guess}")
            print(f"Remaining words: {len(self.allowed_words)}")

            # Update word list based on current guess
            letter_statuses = self.get_letter_stauses(guess)
            self.allowed_words = self.get_new_word_list(guess, letter_statuses)

            # Get next best guess
            if self.allowed_words:
                guess = self.get_best_guess()
                if guess is None:  # Safety check
                    break
            else:
                print("No valid words remaining!")
                break

            self.num_guesses += 1

            # Safety check to avoid infinite loops
            if self.num_guesses >= self.wordle.max_guesses:
                print("Max guesses reached!")
                break

        print(f"Final answer: {guess}")
        print(f"Total guesses: {self.num_guesses + 1}")
        return guess


def simulate(num_runs: int):
    total_guesses = 0
    most_guesses = -1
    for i in range(num_runs):
        print(f"---Simulation {i}---")
        wordle = Wordle()
        solver = Solver(wordle)
        solver.solve()
        total_guesses += solver.num_guesses + 1
        most_guesses = max(most_guesses, solver.num_guesses + 1)

    print(f"Average number of guesses: {round(total_guesses / num_runs, 2)}")
    print(f"Most guesses: {most_guesses}")


if __name__ == "__main__":
    wordle = Wordle(seed=123)
    solver = Solver(wordle)
    solver.user_solve()
