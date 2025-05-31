from game.game import Wordle
import pytest


@pytest.fixture
def wordle():
    return Wordle(seed=12345)


def test_get_secret_word(wordle):
    word = wordle.secret_word
    assert word == "shalt"


def test_validate_guess(wordle):
    assert wordle.is_valid_guess("hell") == False
    assert wordle.is_valid_guess("zzzzz") == False
    assert wordle.is_valid_guess("check") == True


def test_guesses(wordle):
    assert wordle.secret_word == "shalt"
    assert wordle.check_guess("thank") == [1, 2, 2, 0, 0]
    assert wordle.check_guess("again") == [0, 0, 2, 0, 0]
