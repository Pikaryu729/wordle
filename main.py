from solver.solver import Solver
from wordle.wordle import Wordle

if __name__ == "__main__":
    wordle = Wordle()
    solver = Solver(wordle)
    solver.user_solve()
