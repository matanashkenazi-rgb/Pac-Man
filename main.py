import arcade
from pac_man_game import PacmanGame

with open("general.txt", "r") as general_file:
    general_data = general_file.read()
    data = general_data.split("\n")
    WINDOW_WIDTH = int(data[3])
    WINDOW_HEIGHT = int(data[5])

def main():



    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()