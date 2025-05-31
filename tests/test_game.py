from game.game import Game
import pytest

@pytest.fixture
def game():
    return Game(seed=12345)

def test_get_random_word(game):
    word = game.get_random_word() 
    assert word == "pilis"

