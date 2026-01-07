import random

class Character:
    """מחלקת בסיס לדמויות (פקמן, רוחות)."""

    def __init__(self, speed, x, y):
        self.speed = speed

        self.center_x = x
        self.center_y = y

        self.change_x = 0
        self.change_y = 0


class Player(Character):
    """פקמן – השחקן."""

    def __init__(self, x, y):
        super().__init__(speed=2.5, x=x, y=y)

        self.lives = 3
        self.score = 0

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed


class Enemy(Character):
    """רוח שנעה בצורה רנדומלית."""

    def __init__(self, x, y):
        super().__init__(speed=2.0, x=x, y=y)

        # כל כמה זמן מחליפים כיוון
        self.time_to_change_direction = 0.0

    def pick_new_direction(self):
        """בחירת כיוון חדש רנדומלי."""
        directions = [
            (1, 0),   # ימין
            (-1, 0),  # שמאל
            (0, 1),   # למעלה
            (0, -1),  # למטה
            (0, 0),   # לעמוד
        ]
        self.change_x, self.change_y = random.choice(directions)
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self, delta_time=1/60):
        """עדכון תנועת הרוח."""
        self.time_to_change_direction -= delta_time

        if self.time_to_change_direction <= 0:
            self.pick_new_direction()

        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed


class Coin:
    """מטבע לאיסוף."""

    def __init__(self, x, y, value=10):
        self.center_x = x
        self.center_y = y
        self.value = value


class Wall:
    """קיר – חוסם תנועה."""

    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y

# מפה לדוגמה: # = קיר, . = מטבע, P = פקמן, G = רוח, רווח = כלום
LEVEL_MAP = [
    "###########",
    "#P....G...#",
    "#.........#",
    "###########",
]


class ConsolePacmanGame:
    """משחק פקמן טקסטואלי לקונסול."""

    def __init__(self, level_map):
        self.level_map = level_map
        self.height = len(level_map)
        self.width = len(level_map[0]) if self.height > 0 else 0

        self.walls = []
        self.coins = []
        self.ghosts = []
        self.player = None

        # נשמור גם את מיקום ההתחלה של פקמן
        self.start_x = 0
        self.start_y = 0

        self.setup()

    def setup(self):
        """טעינת המפה ויצירת האובייקטים."""
        self.walls = []
        self.coins = []
        self.ghosts = []
        self.player = None

        for y, row in enumerate(reversed(self.level_map)):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.walls.append(Wall(x, y))
                elif cell == ".":
                    self.coins.append(Coin(x, y))
                elif cell == "P":
                    self.player = Player(x, y)
                    self.start_x = x
                    self.start_y = y
                elif cell == "G":
                    self.ghosts.append(Enemy(x, y))

        if self.player is None:
            # אם אין P במפה – שמים במרכז
            self.player = Player(self.width // 2, self.height // 2)
            self.start_x = self.player.center_x
            self.start_y = self.player.center_y

    def render(self):
        """מדפיס את לוח המשחק לקונסול."""
        # נבנה מטריצה ריקה
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # קירות
        for wall in self.walls:
            grid[int(wall.center_y)][int(wall.center_x)] = "#"

        # מטבעות
        for coin in self.coins:
            grid[int(coin.center_y)][int(coin.center_x)] = "."

        # רוחות
        for ghost in self.ghosts:
            grid[int(ghost.center_y)][int(ghost.center_x)] = "G"

        # פקמן (מעל הכל)
        grid[int(self.player.center_y)][int(self.player.center_x)] = "P"

        # הדפסה
        print("\n" + "=" * (self.width + 2))
        for row in reversed(grid):
            print("|" + "".join(row) + "|")
        print("=" * (self.width + 2))
        print(f"Score: {self.player.score} | Lives: {self.player.lives}")

    def is_wall(self, x, y):
        for wall in self.walls:
            if int(wall.center_x) == int(x) and int(wall.center_y) == int(y):
                return True
        return False

    def get_coin_at(self, x, y):
        for coin in self.coins:
            if int(coin.center_x) == int(x) and int(coin.center_y) == int(y):
                return coin
        return None

    def get_ghost_at(self, x, y):
        for ghost in self.ghosts:
            if int(ghost.center_x) == int(x) and int(ghost.center_y) == int(y):
                return ghost
        return None

    def handle_player_move(self, direction):
        """מקבל כיוון ('w','a','s','d') ומזיז את פקמן צעד אחד."""
        dx, dy = 0, 0
        if direction == "w":
            dy = 1
        elif direction == "s":
            dy = -1
        elif direction == "a":
            dx = -1
        elif direction == "d":
            dx = 1
        else:
            return  # כיוון לא חוקי – לא עושים כלום

        new_x = self.player.center_x + dx
        new_y = self.player.center_y + dy

        # בדיקת קיר
        if self.is_wall(new_x, new_y):
            return  # פקמן לא יכול לעבור דרך קירות

        # עדכון מיקום
        self.player.center_x = new_x
        self.player.center_y = new_y

        # בדיקת איסוף מטבע
        coin = self.get_coin_at(new_x, new_y)
        if coin is not None:
            self.player.score += coin.value
            self.coins.remove(coin)

        # בדיקת פגיעה ברוח
        ghost = self.get_ghost_at(new_x, new_y)
        if ghost is not None:
            self.player.lives -= 1
            print("ננגסת ע\"י רוח! חיים -1")
            self.reset_player_position()

    def reset_player_position(self):
        self.player.center_x = self.start_x
        self.player.center_y = self.start_y

    def move_ghosts(self):
        """תזוזת רוחות רנדומלית (צעד אחד בכל תור)."""
        for ghost in self.ghosts:
            # לפעמים מחליפים כיוון
            if random.random() < 0.3 or (ghost.change_x == 0 and ghost.change_y == 0):
                ghost.pick_new_direction()

            new_x = ghost.center_x + ghost.change_x
            new_y = ghost.center_y + ghost.change_y

            # אם יש קיר – לא זזים
            if self.is_wall(new_x, new_y):
                continue

            ghost.center_x = new_x
            ghost.center_y = new_y

            # אם אחרי תזוזה רוח פוגעת בפקמן
            if int(ghost.center_x) == int(self.player.center_x) and int(ghost.center_y) == int(self.player.center_y):
                self.player.lives -= 1
                print("רוח תפסה אותך! חיים -1")
                self.reset_player_position()

    def is_game_over(self):
        if self.player.lives <= 0:
            print("GAME OVER – נגמרו החיים.")
            return True
        if len(self.coins) == 0:
            print("YOU WIN – אספת את כל המטבעות!")
            return True
        return False

    def run(self):
        """לולאת המשחק לקונסול."""
        print("ברוך הבא לפקמן קונסול!")
        print("השליטה: w = למעלה, s = למטה, a = שמאלה, d = ימינה, q = יציאה.")
        while True:
            self.render()

            if self.is_game_over():
                break

            command = input("לאן לזוז? (w/a/s/d/q): ").strip().lower()
            if command == "q":
                print("יציאה מהמשחק.")
                break

            self.handle_player_move(command)
            self.move_ghosts()


if __name__ == "__main__":
    game = ConsolePacmanGame(LEVEL_MAP)
    game.run()