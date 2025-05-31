from game import Game


def main():
    game = Game()
    word = game.get_random_word()
    print(word)

if __name__ == "__main__":
    main()