import pygame
import os

pygame.init()

sprite_path = os.path.dirname(os.path.realpath(__file__)) + r"\Sprites"
font = pygame.font.SysFont(None, 56)


def is_over(m_pos, b_pos, size):
    m_x, m_y = m_pos
    b_x, b_y = b_pos
    wd, ht = size

    if (m_x > b_x and m_x < b_x + wd) and (m_y > b_y and m_y < b_y + ht):
        return True
    else:
        return False


class PopUp:
    def __init__(self, win_size, popup_color):
        self.x_win, self.y_win = win_size
        self.popup_color = popup_color

        self.score_font = pygame.font.SysFont(None, 72)
        self.faded_black = pygame.Surface(win_size, pygame.SRCALPHA)
        self.faded_black.fill((0, 0, 0, 120))
        self.btn_cords = []
        self.on_motions = []
        self.gap = 10

        # Pop Up
        pop_wd, pop_ht = (400, 200)
        self.pop_x = self.x_win / 2 - pop_wd / 2
        self.pop_y = self.y_win / 2 - pop_ht / 2

        self.popup_cords = (self.pop_x, self.pop_y, pop_wd, pop_ht)

        # Buttons
        names = ["Play", "Options", "Menu"]
        wd, ht = (64, 64)

        self.btn_cover = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}/16x16_cover.png"),
            (wd, ht))
        for i, name in enumerate(names):
            fill = self.pop_x + (pop_wd / 2 - wd / 2)

            x = fill + (self.gap + wd) * (i-1)
            y = self.pop_y + pop_ht - ht - self.gap

            img = pygame.transform.scale(
                pygame.image.load(f"{sprite_path}/popup_btn{i+1}.png"),
                (wd, ht)
            )

            self.btn_cords.append([name, x, y, wd, ht, img])
            self.on_motions.append((False, None, None))

    def draw_popup(self, win):
        pygame.draw.rect(win, self.popup_color, self.popup_cords)
    
    def draw_btns(self, win):
        for btn in self.btn_cords:
            name, x, y, wd, ht, img = btn

            win.blit(img, (x, y))

    def draw_score(self, win, scores, icons):
        score, highscore = scores
        food_color, gm = icons

        # Score
        s_text = self.score_font.render(" : " + str(score), True, (0, 0, 0))

        size = s_text.get_height()
        fill = size / 2 - self.gap
        x, y = (self.pop_x + fill, self.pop_y + fill)
        
        pygame.draw.rect(win, food_color, (x, y, size, size))
        win.blit(s_text, (x + size, y))

        # High Score
        hs_text = self.score_font.render(" : " + str(highscore), True, (0, 0, 0))

        size = hs_text.get_height()
        fill = size / 2 - self.gap
        x, y = (self.x_win / 2 + fill, self.pop_y + fill)

        gamemode = pygame.transform.scale(gm, (size, size))

        win.blit(gamemode, (x, y))
        win.blit(hs_text, (x + size, y))


class Menu:
    def __init__(self, win_size):
        self.x_win, self.y_win = win_size

        self.title_font = pygame.font.SysFont(None, 182)
        self.btn_cords = []
        self.on_motions = []
        self.gap = 10

        # Buttons
        names = ["Play", "Options", "Quit"]
        wd, ht = (256, 80)

        self.btn_cover = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}/32x10_cover.png"),
            (wd, ht))
        for i, name in enumerate(names):
            x = self.x_win / 2 - wd / 2
            y = self.y_win / 2 - ht / 2 - ht + (ht + self.gap) * i

            img = pygame.transform.scale(
                pygame.image.load(f"{sprite_path}/menu_btn{i+1}.png"),
                (wd, ht)
            )

            self.btn_cords.append([name, x, y, wd, ht, img])
            self.on_motions.append(tuple())

    def draw_title(self, win):
        text = self.title_font.render("Snake", True, (0, 0, 0))

        win.blit(text, (self.x_win / 2 - text.get_width() / 2, 15))

    def draw_btns(self, win):
        for cords in self.btn_cords:
            name, x, y, wd, ht, img = cords

            win.blit(img, (x, y))


class Settings:
    def __init__(self, win_size):
        self.x_win, self.y_win = win_size

        self.btn_cords = [
            ["Volume", True],
            ["Color Mode", True],
            ["Quit", False]]
        self.on_motions = []
        self.gap = 10
        
        self.menu_btn_cover = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}/16x16_cover.png"),
            (64, 64))
        self.game_btn_cover = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}/16x16_cover.png"),
            (32, 32))

        # Setting Buttons
        for i, cords in enumerate(self.btn_cords, 1):
            self.update_btns(cords, i, True)
            self.on_motions.append((False, None, None))

    def update_btns(self, cords, pos, in_menu, win=False):
        # Coordinates
        if in_menu:
            wd, ht = (64, 64)

            x = self.x_win - (wd * pos) - (self.gap * pos)
            y = self.y_win - ht - self.gap
        else:
            wd, ht = (32, 32)

            x = self.x_win - (40 * pos) - ht
            y = self.y_win - (40 / 2 + ht / 2)

        # Image
        if cords[1]:
            toggle = "on"
        else:
            toggle = "off"

        img = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}/setting_btn{pos}_{toggle}.png"),
            (wd, ht))

        # Draw or Declare
        if win:
            win.blit(img, (x, y))

            # Update Cords
            new = [x, y, wd, ht]
            for i in range(2, len(cords) - 1):
                cords[i] = new[i-2]
        else:
            cords.extend([x, y, wd, ht])

    def draw_btns(self, win, in_menu):
        # Setting Buttons
        for i, cords in enumerate(self.btn_cords, 1):
            if in_menu and i == 3:
                break
            else:
                self.update_btns(cords, i, in_menu, win)


class Options:
    def __init__(self, win_size, window_color):
        self.x_win, self.y_win = win_size
        self.window_color = window_color

        self.title_font = pygame.font.SysFont(None, 92)
        self.subtitle_font = pygame.font.SysFont(None, 46)
        self.win_from = None
        self.gap = 22
        self.line = self.y_win / 7

        # QUIT BUTTON
        x, y = (10, 10)
        wd, ht = (48, 48)

        img = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}/setting_btn3_off.png"),
            (wd, ht))
        self.btn_cover = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}/16x16_cover.png"),
            (wd, ht))

        self.quit_cords = (x, y, wd, ht, img)
        self.on_motion = (False, None, None)

        # OPTION BUTTONS
        self.gamemode = [
            [True, 1],  # normal
            [False, 2],  # appering walls
            [False, 3],  # cheese body
            [False, 4],  # you are the food
            [False, 5],  # 2 players
            [False, 6]]  # peacefull
        self.snake_col = [
            [False, (199, 15, 21), (163, 0, 5)],  # red
            [False, (233, 111, 27), (207, 84, 2)],  # orange
            [False, (245, 245, 137), (209, 209, 50)],  # yellow
            [False, (96, 160, 64), (56, 116, 26)],  # green
            [True, (46, 140, 212), (20, 100, 161)],  # blue
            [False, (146, 42, 149), (105, 30, 107)],  # pruple
            [False, (25, 25, 25), (0, 0, 0)],  # black
            [False, (225, 225, 225), (175, 175, 175)]]  # white
        self.food_col = [
            [True, (199, 15, 21)],  # red
            [False, (233, 111, 27)],  # orange
            [False, (245, 245, 137)],  # yellow
            [False, (96, 160, 64)],  # green
            [False, (46, 140, 212)],  # blue
            [False, (146, 42, 149)],  # pruple
            [False, (25, 25, 25)],  # black
            [False, (225, 225, 225)]]  # white
        self.num_food = [
            [True, 1],  # 1
            [False, 3],  # 3
            [False, 5]]  # 5
        self.speed = [
            [False, 6],  # slow
            [True, 10],  # normal
            [False, 14]]  # fast
        self.board_sz = [
            [False, 10],  # small
            [True, 20],  # normal
            [False, 30]]  # large
 
        # Gamemodes
        for i, cords in enumerate(self.gamemode):
            self.update_btns(cords, (i, 1), ("mode", i+1))

        # Snake Color
        for i, cords in enumerate(self.snake_col):
            self.update_btns(cords, (i, 2))

        # Food Color
        for i, cords in enumerate(self.food_col):
            self.update_btns(cords, (i, 3))
 
        # Number of Food
        for i, cords in enumerate(self.num_food):
            self.update_btns(cords, (i, 4), ("food", i+1))

        # Speed
        for i, cords in enumerate(self.speed):
            self.update_btns(cords, (i, 5), ("speed", i+1))

        # Board Size
        for i, cords in enumerate(self.board_sz):
            self.update_btns(cords, (i, 6), ("board", i+1))

    def update_btns(self, cords, pos, img_data=False, win=False):
        x_pos, y_pos = pos

        if cords[0]:
            wd, ht = (64, 64)
        else:
            wd, ht = (32, 32)

        x = (self.gap + (self.gap + 58) * x_pos) + 58 / 2 - wd / 2
        y = self.line * y_pos + self.line / 2 - ht / 2

        if img_data:
            img_name, img_pos = img_data

            img = pygame.transform.scale(
                pygame.image.load(f"{sprite_path}/{img_name}{img_pos}.png"),
                (wd, ht))

            if win:
                win.blit(img, (x, y))

                new = [x, y, wd, ht]
                for i in range(3, len(cords)):
                    cords[i] = new[i-3]
            else:
                cords.extend([img, x, y, wd, ht])
        else:
            if win:
                pygame.draw.rect(win, cords[1], (x, y, wd, ht))

                new = [x, y, wd, ht]
                if len(cords) == 6:
                    j = 1
                else:
                    j = 0

                for i in range(3-j, len(cords)):
                    cords[i] = new[i - (3-j)]
            else:
                cords.extend([x, y, wd, ht])

    def draw_lines(self, win):
        lines = (self.y_win / 7)

        for i in range(1, 7):
            line = lines * i
            pygame.draw.line(win, (30, 30, 30), (0, line), (self.x_win, line), 3)

        values = ["Gamemodes", "Snake Color", "Food Color", "Number of Food", "Speed", "Board Size"]
        for i, value in enumerate(values, 1):
            line = lines * i

            text = self.subtitle_font.render(value, True, (0, 0, 0))
            x, y = (50, line - text.get_height() / 2)
            bg_wd = text.get_width() + 25
            bg_ht = text.get_height()

            pygame.draw.rect(
                win, self.window_color, 
                (x - (bg_wd / 2 - text.get_width() / 2), y, 
                bg_wd, bg_ht)
            )
            win.blit(text, (x, y))

    def draw_title(self, win):
        text = self.title_font.render("Options", True, (0, 0, 0))

        win.blit(
            text, 
            (self.x_win / 2 - text.get_width() / 2, 
            self.y_win / 7 / 2 - text.get_height() / 2)
        )

    def draw_btns(self, win):
        # Gamemode Buttons
        for i, cords in enumerate(self.gamemode):
            self.update_btns(cords, (i, 1), ("mode", i+1), win)

        # Snake Color Buttons
        for i, cords in enumerate(self.snake_col):
            self.update_btns(cords, (i, 2), False, win)

        # Food Color Buttons
        for i, cords in enumerate(self.food_col):
            self.update_btns(cords, (i, 3), False, win)

        # Number of Food Buttons
        for i, cords in enumerate(self.num_food):
            self.update_btns(cords, (i, 4), ("food", i+1), win)

        # Speed Buttons
        for i, cords in enumerate(self.speed):
            self.update_btns(cords, (i, 5), ("speed", i+1), win)

        # Board Size
        for i, cords in enumerate(self.board_sz):
            self.update_btns(cords, (i, 6), ("board", i+1), win)


        # Quit Button
        x, y, wd, ht, img = self.quit_cords

        win.blit(img, (x, y))