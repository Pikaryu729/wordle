# 🧠 Wordle Solver

A smart and efficient solver for the popular word puzzle game **Wordle**. This project uses logic and probability to find the optimal guess for each round.

---

## 🎯 Features

- ✅ Solves standard 5-letter Wordle puzzles
- 📈 Smart scoring/heuristics to select optimal guesses
- 🧪 Easy to test and extend

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- `pip` installed

### Installation

This project uses uv and project.toml for dependency management. uv is a fast python package manager built in rust

#### 1. Install uv

if you don't have uv installed:
follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/):

#### 2. Clone the repository

```bash
git clone https://github.com/pikaryu729/wordle-solver.git
cd wordle-solver
```

#### 3. Create a virtual environment

```bash
uv venv
source .venv/vin/activate
```

#### 4. Install dependencies

```bash
uv pip install -e .
```

Thats it! you're ready to run the solver

## 🧩 Usage

Run the solver

```bash
python3 main.py
Guess Number 1
Starting Guess: tares
Enter list of numbers: 0 - grey, 1 - yellow, 2 - green:
```

enter the starting guess "tares" into the wordle program, and enter your result.
for example if you get this:
![Example wordle](/images/example-wordle.png)

You would enter like this:

```bash

Enter list of numbers: 0 - grey, 1 - yellow, 2 - green: 02001
Guess number 2
Best Guess: salsa
```

Repeat until it finds the answer.

## 📚 How it works:

1. The solver finds the word with the most entropy in it's current word list
2. Solver updates word list by removing all impossible words
3. Repeat
