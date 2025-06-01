import math
from collections import defaultdict
from wordle.wordle import Wordle
from solver.analysis import count_num_words_with_letter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def check_guess(guess: str, answer: str) -> tuple[int]:
    """
    output list of numbers where:
    0 - character is not in word.
    1 - character is in word but at wrong possition.
    2 - character is in word, at right position
    """
    word_counts = {}
    out = [0] * len(guess)

    for char in answer:
        word_counts[char] = word_counts.get(char, 0) + 1

    for i, char in enumerate(guess):
        if char == answer[i] and word_counts[char] > 0:
            word_counts[char] -= 1
            out[i] = 2

    for i, char in enumerate(guess):
        if out[i] != 2 and char in answer and word_counts[char] > 0:
            word_counts[char] -= 1
            out[i] = 1

    return tuple(out)

def get_guess_entropy(guess: str, allowed_words: list[str]) -> float:
    if not allowed_words:
        return 0.0

    pattern_counts = defaultdict(int)
    for word in allowed_words:
        pattern = check_guess(guess, word)
        pattern_counts[pattern] += 1 

    entropy = 0.0
    total_words = len(allowed_words)

    for count in pattern_counts.values():
        if count > 0:  # Avoid log(0)
            probability = count / total_words
            entropy -= probability * math.log2(probability)
    
    return entropy

def get_new_word_list(guess: str, allowed_words: list[str], secret_word: str) -> list[str]:
    letter_statuses = check_guess(guess, secret_word)
    return filter_words_by_response(guess, letter_statuses, allowed_words)

def filter_words_by_response(guess: str, response: tuple, word_list: list[str]) -> list[str]:
    """
    Filter word list to only include words that would give the specified response to the guess.
    Useful for updating the possible word list after each guess.
    """
    return [word for word in word_list if check_guess(guess, word) == response]


if __name__ == "__main__":
    total_num_guesses = 0
    wordle = Wordle(seed=123)
    guess = "tares"
    word_list = wordle.allowed_words
    while guess != wordle.secret_word:
        word_list = get_new_word_list(guess, word_list, wordle.secret_word)
        entropy_table = {guess:get_guess_entropy(guess, word_list) for guess in word_list }
        guess = max(entropy_table, key=entropy_table.get)
        total_num_guesses += 1
    print(guess)
