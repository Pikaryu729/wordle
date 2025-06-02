import pytest
from wordle.wordle import Wordle


def test_get_secret_word(wordle):
    word = wordle.secret_word
    assert word == "melas"


def test_validate_guess(wordle):
    assert wordle.is_valid_guess("hell") == False
    assert wordle.is_valid_guess("zzzzz") == False
    assert wordle.is_valid_guess("check") == True


def test_guesses(wordle):
    wordle.secret_word = "lenes"
    assert wordle.check_guess("thank") == [0, 0, 0, 1, 0]
    assert wordle.check_guess("again") == [0, 0, 0, 0, 1]
    assert wordle.check_guess("guess") == [0, 0, 1, 0, 2]
    assert wordle.check_guess("quips") == [0, 0, 0, 0, 2]
    wordle.secret_word = "abide"
    assert wordle.check_guess("speed") == [0, 0, 1, 0, 1]
    wordle.secret_word = "erase"
    assert wordle.check_guess("speed") == [1, 0, 1, 1, 0]
