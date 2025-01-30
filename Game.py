import pygame
import os

pygame.init()

audio_path = os.path.dirname(os.path.realpath(__file__)) + r"\Audio"


class Game:
    # Sounds
    left_sound = pygame.mixer.Sound(audio_path + r"\left turn.mp3")
    right_sound = pygame.mixer.Sound(audio_path + r"\right turn.mp3")
    up_sound = pygame.mixer.Sound(audio_path + r"\up turn.mp3")
    down_sound = pygame.mixer.Sound(audio_path + r"\down turn.mp3")
    eat_sound = pygame.mixer.Sound(audio_path + r"\eat.mp3")
    bump_sound = pygame.mixer.Sound(audio_path + r"\bumped.mp3")

    def __init__(self):
        self.window_color = (58, 72, 89)
        self.dark_tile = (32, 41, 55)
        self.light_tile = (38, 52, 69)

        self.score_font = pygame.font.SysFont(None, 45)
        self.score = 0

        self.high_scores = [0, 0, 0, 0, 0, 0]

    def draw_board(self, win, cells, tile, gap):
        for x in range(cells):
            for y in range(cells):
                if (x+y) % 2 == 0:
                    color = self.dark_tile
                else:
                    color = self.light_tile

                pygame.draw.rect(
                    win, color,
                    ((x * tile) + gap,
                    (y * tile) + gap,
                    tile, tile)
                )

    def draw_score(self, win, cells, tile, gap, gamemode):
        s_text = self.score_font.render(
            "Score: " + str(self.score), 
            True, 
            (0, 0, 0)
        )
        win.blit(
            s_text, 
            (gap, 
            gap / 2 - s_text.get_height() / 2)
        )

        high_score = self.high_scores[gamemode-1]
        hs_text = self.score_font.render(
            "High Score: " + str(high_score), 
            True, 
            (0, 0, 0)
        )
        win.blit(
            hs_text, 
            (tile * cells - hs_text.get_width() + gap, 
            gap / 2 - s_text.get_height() / 2)
        )

    def reset(self, cells, entities, gamemode):
        snake1, snake2, food, walls = entities

        # Score
        self.score = 0
        
        # Snake
        snake1.length = 1
        snake1.pos = [snake1.top_p]
        snake1.facing = snake1.right
        snake1.status = True

        snake2.length = 1
        snake2.pos = [snake2.bot_p]
        snake2.facing = snake2.left
        snake2.status = True

        # Food
        entities_pos = []

        for pos in snake1.pos:
            entities_pos.append(pos)

        if gamemode == 5:
            for pos in snake2.pos:
                entities_pos.append(pos)

        for f in food:
            entities_pos.append(f.pos)

        for f in food:
            f.randomize(cells, entities_pos)

        # Walls
        walls.clear()
