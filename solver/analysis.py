import math


# counts number of words with the given character in words
def count_num_words_with_letter(char: str, words: list[str]):
    return sum([1 for word in words if char in word])


def print_prob_table(prob_table: dict[str, float]):
    for letter, prob in prob_table.items():
        print(f"{letter}: {prob}")


def calculate_entropy(letter: str, prob_table: dict[str, float]):
    prob_contains = prob_table[letter]
    prob_not_contains = 1 - prob_table[letter]
    return -sum(
        [
            prob_contains * math.log2(prob_contains),
            prob_not_contains * math.log2(prob_not_contains),
        ]
    )


def build_entropy_dict(all_letters):
    entropy_dict = {
        letter: round(calculate_entropy(letter), 3) for letter in all_letters
    }
    return entropy_dict
