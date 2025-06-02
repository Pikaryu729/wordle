import pytest
from solver.solver import Solver
from wordle.wordle import Wordle


@pytest.fixture
def wordle():
    return Wordle(seed=12345)


@pytest.fixture
def solver(wordle):
    return Solver(wordle)
