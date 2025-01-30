from random import choice
import pygame
import os

sprite_path = os.path.dirname(os.path.realpath(__file__)) + r"\Sprites"


class Snake:
    # Directions
    left = (-1, 0)
    right = (1, 0)
    up = (0, -1)
    down = (0, 1)

    def __init__(self, is_top):
        self.is_top = is_top

        self.top_p = (0, 1)
        self.bot_p = (8, 7)  # (19, 18)

        if self.is_top:
            self.body_color = (46, 140, 212)
            self.head_color = (3, 78, 135)  
            self.pos = [self.top_p]
            self.facing = self.right
        else:
            self.body_color = (199, 15, 21)
            self.head_color = (163, 0, 5)  
            self.pos = [self.bot_p]
            self.facing = self.left

        self.length = 1
        self.status = True

    def draw(self, win, tile, gap, char):
        for i, p in enumerate(self.pos):
            x, y = p

            pygame.draw.rect(
                win, self.body_color,
                ((x * tile) + (tile / 2 - char / 2) + gap,
                (y * tile) + (tile / 2 - char / 2) + gap,
                char, char)
            )
        else:
            x, y = self.get_head()

            pygame.draw.rect(
                    win, self.head_color,
                    ((x * tile) + (tile / 2 - char / 2) + gap,
                    (y * tile) + (tile / 2 - char / 2) + gap,
                    char, char)
                )

    def get_head(self):
        return self.pos[0]

    def turn(self, direction):
        i, j = direction
        if self.length > 1 and (i * -1, j * -1) == self.facing:
            return
        else:
            self.facing = direction

    def move(self, cells, gamemode):
        f_x, f_y = self.facing

        # Cheese
        if gamemode == 3:
            for i, pos in enumerate(self.pos):
                x, y = pos

                if i != 0 and (x+y) % 2 != 0:
                    self.pos.pop(i)

        x, y = self.get_head()

        if x == 0 and self.facing == self.left:
            if gamemode != 6:
                self.status = False
                return
            else:
                x = cells
        elif x == cells - 1 and self.facing == self.right:
            if gamemode != 6:
                self.status = False
                return
            else:
                x = -1
        elif y == 0 and self.facing == self.up:
            if gamemode != 6:
                self.status = False
                return
            else:
                y = cells
        elif y == cells - 1 and self.facing == self.down:
            if gamemode != 6:
                self.status = False
                return
            else:
                y = -1

        new = (x + f_x, y + f_y)

        # Walls
        if type(gamemode) == tuple and gamemode[0] == 2:
            gm, walls = gamemode

            wall_pos = []
            for wall in walls:
                wall_pos.append(wall.pos)

            if new in wall_pos:
                self.status = False
                return

        # Multiplayer
        if type(gamemode) == tuple and gamemode[0] == 5:
            gm, snake2_pos = gamemode 

            if new in self.pos[:] or new in snake2_pos[:]:
                self.status = False
                return
            else:
                self.pos.insert(0, new)
                if len(self.pos) > self.length:
                    self.pos.pop()
        # Peacefull
        elif gamemode == 6:
            self.pos.insert(0, new)
            if len(self.pos) > self.length:
                self.pos.pop()
        # Any Other
        else:
            if len(self.pos) > 2 and new in self.pos[2:]:
                self.status = False
                return
            else:
                self.pos.insert(0, new)
                if len(self.pos) > self.length:
                    self.pos.pop()


class Food:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self):
        self.color = (199, 15, 21)

    def draw(self, win, tile, gap, char):
        x, y = self.pos

        pygame.draw.rect(
            win, self.color,
            ((x * tile) + (tile / 2 - char / 2) + gap,
            (y * tile) + (tile / 2 - char / 2) + gap,
            char, char)
        )
    
    def move(self, cells, snake_pos):
        x, y = self.pos

        possibles = []

        for facing in self.directions:
            f_x, f_y = facing

            n_x = x + f_x
            n_y = y + f_y
            
            # if New Positions is in Board;
            # New Positions not in Snake
            if n_x != cells and n_x != -1 and n_y != cells and n_y != -1 and (n_x, n_y) not in snake_pos:
                possibles.append((n_x, n_y))

        if len(possibles) != 0:
            self.pos = choice(possibles)

    def randomize(self, cells, entities_pos):
        boxes = [(x, y) for x in range(cells) for y in range(cells) if (x, y) not in entities_pos]

        self.pos = choice(boxes)


class Wall:
    def __init__(self, color, tile):
        self.color = color
        
        self.wall = pygame.transform.scale(
            pygame.image.load(f"{sprite_path}\wall.png"),
            (int(tile), int(tile))
        )

    def draw(self, win, tile, gap, char, window_color):
        x, y = self.pos

        pygame.draw.rect(
            win, window_color, 
            (x * tile + gap, y * tile + gap, 
            tile, tile)
        )

        win.blit(
            self.wall,
            (x * tile + gap,
            y * tile + gap)
        )

    def randomize(self, cells, entities_pos):
        boxes = [(x, y) for x in range(cells) for y in range(cells) if (x, y) not in entities_pos]

        self.pos = choice(boxes)
