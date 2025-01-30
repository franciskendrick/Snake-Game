from Windows import PopUp, Menu, Options, Settings
from Windows import is_over
from Game import Game
from Entities import Snake, Food, Wall
import pygame
import os

pygame.init()


def update_game():
    global gamemode, gm_icon, food
    global fps, cells, tile, char

    # Gamemodes
    for cords in gamemodes:
        if cords[0]:
            gamemode = cords[1]
            gm_icon = cords[2]
            break

    # Number of Food
    food = []
    for cords in num_food:
        if cords[0]:
            n = cords[1]
            break

    for i in range(n):
        food.append(Food())

    # Food Color
    for cords in food_color:
        if cords[0]:
            color = cords[1]
            break

    for f in food:
        f.color = color

    # Snake Color
    for cords in snake_color:
        if cords[0]:
            snake1.body_color = cords[1]
            snake1.head_color = cords[2]
            break

    # Speed
    for cords in speed:
        if cords[0]:
            fps = cords[1]
            break 

    # Board Size
    for cords in board_size:
        if cords[0]:
            cells = cords[1]
            tile = (x_win - gap * 2) / cells
            char = tile * 0.80
            break

def update_windows():
    pop_up.popup_color = game.window_color
    options.window_color = game.window_color


x_win, y_win = (680, 680)
win_size = (x_win, y_win)

sprite_path = os.path.dirname(os.path.realpath(__file__)) + r"\Sprites"
icon = pygame.image.load(f"{sprite_path}\icon.png")

win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Pygame Snake")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

gap = 40

# Game
game = Game()

# Windows
menu = Menu(win_size)
settings = Settings(win_size)
pop_up = PopUp(win_size, game.window_color)
options = Options(win_size, game.window_color)

gamemodes = options.gamemode
food_color = options.food_col
snake_color = options.snake_col
num_food = options.num_food
speed = options.speed
board_size = options.board_sz

update_windows()

# Entities
walls = []
snake1 = Snake(True)
snake2 = Snake(False)

update_game()


# Redraws
def redraw_game():
    win.fill(game.window_color)

    game.draw_board(win, cells, tile, gap)
    game.draw_score(win, cells, tile, gap, gamemode)

    for f in food:
        f.draw(win, tile, gap, char)

    snake1.draw(win, tile, gap, char)

    if gamemode == 5:
        snake2.draw(win, tile, gap, char)

    if gamemode == 2:
        for wall in walls:
            wall.draw(win, tile, gap, char, game.window_color)

    settings.draw_btns(win, False)

    # Setting Buttons
    for on_motion in settings.on_motions:
        is_over, x, y = on_motion

        if is_over:
            win.blit(settings.game_btn_cover, (x, y))

def redraw_lost():
    win.blit(pop_up.faded_black, (0, 0)) 

    pop_up.draw_popup(win)
    pop_up.draw_btns(win)
    pop_up.draw_score(
        win, 
        (game.score, game.high_scores[gamemode-1]), 
        (food[0].color, gm_icon))

    # Pop-Up Buttons
    for on_motion in pop_up.on_motions:
        is_over, x, y = on_motion

        if is_over:
            win.blit(pop_up.btn_cover, (x, y))

    settings.draw_btns(win, False)

    # Setting Buttons
    for on_motion in settings.on_motions:
        is_over, x, y = on_motion

        if is_over:
            win.blit(settings.game_btn_cover, (x, y))

def redraw_menu():
    win.fill(game.window_color)

    menu.draw_title(win)
    menu.draw_btns(win)

    # Menu Buttons
    for on_motion in menu.on_motions:
        is_over, x, y = on_motion

        if is_over:
            win.blit(menu.btn_cover, (x, y))

    settings.draw_btns(win, True)

    # Setting Buttons
    for i, on_motion in enumerate(settings.on_motions):
        if i == 2:
            break
        else:
            is_over, x, y = on_motion

            if is_over:
                win.blit(settings.menu_btn_cover, (x, y))

def redraw_options():
    win.fill(game.window_color)

    options.draw_lines(win)
    options.draw_title(win)
    options.draw_btns(win)

    is_over, x, y = options.on_motion
    if is_over:
        win.blit(options.btn_cover, (x, y))


# Loops
def game_loop():
    run_game = True

    update_game()
    count = 1

    # Food
    entities_pos = []

    for pos in snake1.pos:
        entities_pos.append(pos)

    for f in food:
        try:
            entities_pos.append(list(f.pos))
        except AttributeError:
            pass

        f.randomize(cells, entities_pos)


    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            m_pos = pygame.mouse.get_pos()

            # Snake Handle Keys
            if event.type == pygame.KEYDOWN:
                if gamemode == 5:
                    if event.key == pygame.K_LEFT:
                        snake1.turn(snake1.left)
                        if settings.btn_cords[0][1]:
                            game.left_sound.play()
                    elif event.key == pygame.K_RIGHT:
                        snake1.turn(snake1.right)
                        if settings.btn_cords[0][1]:
                            game.right_sound.play()
                    elif event.key == pygame.K_UP:
                        snake1.turn(snake1.up)
                        if settings.btn_cords[0][1]:
                            game.up_sound.play()
                    elif event.key == pygame.K_DOWN:
                        snake1.turn(snake1.down)
                        if settings.btn_cords[0][1]:
                            game.down_sound.play()

                    if event.key == pygame.K_a:
                        snake2.turn(snake2.left)
                        if settings.btn_cords[0][1]:
                            game.left_sound.play()
                    elif event.key == pygame.K_d:
                        snake2.turn(snake2.right)
                        if settings.btn_cords[0][1]:
                            game.right_sound.play()
                    elif event.key == pygame.K_w:
                        snake2.turn(snake2.up)
                        if settings.btn_cords[0][1]:
                            game.up_sound.play()
                    elif event.key == pygame.K_s:
                        snake2.turn(snake2.down)
                        if settings.btn_cords[0][1]:
                            game.down_sound.play()
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake1.turn(snake1.left)
                        if settings.btn_cords[0][1]:    
                            game.left_sound.play()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake1.turn(snake1.right) 
                        if settings.btn_cords[0][1]:    
                            game.right_sound.play()            
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake1.turn(snake1.up)
                        if settings.btn_cords[0][1]:    
                            game.up_sound.play()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake1.turn(snake1.down)
                        if settings.btn_cords[0][1]:    
                            game.down_sound.play()

            # Setting Buttons
            for i, btn in enumerate(settings.btn_cords):
                name, status, x, y, wd, ht = btn 

                # if Mouse is Hovering
                if event.type == pygame.MOUSEMOTION and is_over(m_pos, (x, y), (wd, ht)):
                    settings.on_motions[i] = (True, x, y)
                else:
                    settings.on_motions[i] = (False, None, None)

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    if name == "Volume":
                        if status:  # Muted
                            btn[1] = False
                        else:  # Un-mute
                            btn[1] = True
                    elif name == "Color Mode":
                        if status:  # Dark
                            btn[1] = False

                            game.window_color = (87, 138, 52)
                            game.dark_tile = (136, 184, 46)
                            game.light_tile = (156, 201, 66)
                        else:  # Light
                            btn[1] = True

                            game.window_color = (58, 72, 89)
                            game.dark_tile = (32, 41, 55)
                            game.light_tile = (38, 52, 69)

                        update_windows()
                    elif name == "Quit":
                        lost_loop()

        # Move Entities
        if gamemode == 2:
            snake1.move(cells, (gamemode, walls))
        elif gamemode == 4:
            snake1.move(cells, gamemode)

            if count % 3 == 0:
                for f in food:
                    f.move(cells, snake1.pos)
                count = 1
            else:
                count += 1
        elif gamemode == 5:
            snake1.move(cells, (gamemode, snake2.pos))
            snake2.move(cells, (gamemode, snake1.pos))
        else:
            snake1.move(cells, gamemode)   

        # if Player Lost
        if not snake1.status or not snake2.status:
            if settings.btn_cords[0][1]:
                game.bump_sound.play()
            lost_loop()

        # if Player Ate Food
        for i, f in enumerate(food):
            if gamemode == 5:
                snakes = [snake1, snake2]
            else:
                snakes = [snake1]

            if snake1.get_head() == f.pos:
                # Score
                if game.score >= game.high_scores[gamemode-1]:
                    game.high_scores[gamemode-1] += 1
                game.score += 1

                # Snake
                snake1.length += 1
                if settings.btn_cords[0][1]:
                    game.eat_sound.play()

                # Food
                entities_pos = []
                for pos in snake1.pos:
                    entities_pos.append(pos)

                for pos in snake2.pos:
                    entities_pos.append(pos)

                for f in food:
                    entities_pos.append(f.pos)

                if gamemode == 2:
                    for wall in walls:
                        entities_pos.append(wall.pos)

                food[i].randomize(cells, entities_pos)
            elif snake2.get_head() == f.pos:
                # Score
                if game.score >= game.high_scores[gamemode-1]:
                    game.high_scores[gamemode-1] += 1
                game.score += 1

                # Snake
                snake2.length += 1
                if settings.btn_cords[0][1]:
                    game.eat_sound.play()

                # Food
                entities_pos = []
                for pos in snake1.pos:
                    entities_pos.append(pos)

                for pos in snake2.pos:
                    entities_pos.append(pos)

                for f in food:
                    entities_pos.append(f.pos)

                food[i].randomize(cells, entities_pos)

        if gamemode == 2:
            # Score is Even;
            # Score == Number of Walls,
            # then Create a Wall
            if game.score % 2 == 0 and game.score > 0 and game.score // 2 == len(walls) + 1:
                entities_pos = []

                for pos in snake1.pos:
                    entities_pos.append(pos)

                for f in food:
                    entities_pos.append(f.pos)

                for wall in walls:
                    entities_pos.append(wall.pos)

                walls.append(Wall(game.window_color, tile))
                walls[-1].randomize(cells, entities_pos)

        redraw_game()
        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    quit()

def lost_loop():
    run_lost = True

    while run_lost:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_lost = False

            m_pos = pygame.mouse.get_pos()

            # Pop-Up Buttons
            for i, btn in enumerate(pop_up.btn_cords):
                name, x, y, wd, ht, img = btn

                # if Mouse is Hovering
                if event.type == pygame.MOUSEMOTION and is_over(m_pos, (x, y), (wd, ht)):
                    pop_up.on_motions[i] = (True, x, y)
                else:
                    pop_up.on_motions[i] = (False, None, None)

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    if name == "Play":
                        game.reset(cells, (snake1, snake2, food, walls), gamemode-1)
                        game_loop()
                    elif name == "Options":
                        options.win_from = "Game"
                        options_loop()
                    elif name == "Menu":
                        game.reset(cells, (snake1, snake2, food, walls), gamemode-1)
                        menu_loop()

            # Setting Buttons
            for i, btn in enumerate(settings.btn_cords):
                name, status, x, y, wd, ht = btn 

                # if Mouse is Hovering
                if event.type == pygame.MOUSEMOTION and is_over(m_pos, (x, y), (wd, ht)):
                    settings.on_motions[i] = (True, x, y)
                else:
                    settings.on_motions[i] = (False, None, None)

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    if name == "Volume":
                        if status:  # Muted
                            btn[1] = False
                        else:  # Un-mute
                            btn[1] = True
                    elif name == "Color Mode":
                        if status:  # Dark
                            btn[1] = False

                            game.window_color = (87, 138, 52)
                            game.dark_tile = (136, 184, 46)
                            game.light_tile = (156, 201, 66)
                        else:  # Light
                            btn[1] = True

                            game.window_color = (58, 72, 89)
                            game.dark_tile = (32, 41, 55)
                            game.light_tile = (38, 52, 69)

                        update_windows()
                    elif name == "Quit":
                        run_lost = False

        redraw_game()
        redraw_lost()
        pygame.display.update()

    pygame.quit()
    quit()

def menu_loop():
    run_menu = True

    while run_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False

            m_pos = pygame.mouse.get_pos()

            # Menu Buttons
            for i, btn in enumerate(menu.btn_cords):
                name, x, y, wd, ht, img = btn

                # if Mouse is Hovering
                if event.type == pygame.MOUSEMOTION and is_over(m_pos, (x, y), (wd, ht)):
                    menu.on_motions[i] = (True, x, y)
                else:
                    menu.on_motions[i] = (False, None, None)

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    if name == "Play":
                        game_loop()
                    elif name == "Options":
                        options.win_from = "Menu"
                        options_loop()
                    elif name == "Quit":
                        run_menu = False

            # Setting Buttons
            for i, btn in enumerate(settings.btn_cords):
                name, status, x, y, wd, ht = btn 

                # if Mouse is Hovering
                if event.type == pygame.MOUSEMOTION and is_over(m_pos, (x, y), (wd, ht)):
                    settings.on_motions[i] = (True, x, y)
                else:
                    settings.on_motions[i] = (False, None, None)

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    if name == "Volume":
                        if status:  # Muted
                            btn[1] = False
                        else:  # Un-mute
                            btn[1] = True
                    elif name == "Color Mode":
                        if status:  # Light
                            btn[1] = False

                            game.window_color = (87, 138, 52)
                            game.dark_tile = (136, 184, 46)
                            game.light_tile = (156, 201, 66)
                        else:  # Dark
                            btn[1] = True

                            game.window_color = (58, 72, 89)
                            game.dark_tile = (32, 41, 55)
                            game.light_tile = (38, 52, 69)

                        update_windows()

        redraw_menu()
        pygame.display.update()

    pygame.quit()
    quit()

def options_loop():
    run_options = True

    while run_options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_options = False

            m_pos = pygame.mouse.get_pos()

            # QUIT BUTTON
            x, y, wd, ht, img = options.quit_cords

            # if Mouse is Hovering
            if event.type == pygame.MOUSEMOTION and is_over(m_pos, (x, y), (wd, ht)):
                options.on_motion = (True, x, y)
            else:
                options.on_motion = (False, None, None)

            # if Quit is Clicked
            if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                if options.win_from == "Game":
                    lost_loop()
                elif options.win_from == "Menu":
                    menu_loop()


            # GAMEMODE BUTTONS
            for btn in gamemodes:
                selected, value, img, x, y, wd, ht = btn
                btn = gamemodes[gamemodes.index(btn)]

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    for i, data in enumerate(gamemodes):
                        if data[0]:
                            data[0] = False
                            break

                    idx = gamemodes.index(btn)
                    gamemodes[idx][0] = True

            # FOOD COLOR BUTTONS
            for btn in food_color:
                selected, color, x, y, wd, ht = btn
                btn = food_color[food_color.index(btn)]

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    for i, data in enumerate(food_color):
                        if data[0]:
                            data[0] = False
                            break

                    idx = food_color.index(btn)
                    food_color[idx][0] = True

            # snake1 COLOR BUTTONS    
            for btn in snake_color:
                selected, body, head, x, y, wd, ht = btn
                btn = snake_color[snake_color.index(btn)]

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    for i, data in enumerate(snake_color):
                        if data[0]:
                            data[0] = False
                            break
                    
                    idx = snake_color.index(btn)
                    snake_color[idx][0] = True
                    
            # NUMBER OF FOOD BUTTONS
            for btn in num_food:
                selected, value, img, x, y, wd, ht = btn
                btn = num_food[num_food.index(btn)]

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    for i, data in enumerate(num_food):
                        if data[0]:
                            data[0] = False
                            break

                    idx = num_food.index(btn)
                    num_food[idx][0] = True

            # SPEED BUTTONS
            for btn in speed:
                selected, value, img, x, y, wd, ht = btn
                btn = speed[speed.index(btn)]

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    for i, data in enumerate(speed):
                        if data[0]:
                            data[0] = False
                            break

                    idx = speed.index(btn)
                    speed[idx][0] = True

            # BOARD SIZE BUTTONS
            for btn in board_size:
                selected, value, img, x, y, wd, ht = btn
                btn = board_size[board_size.index(btn)]

                # if Button is Clicked
                if event.type == pygame.MOUSEBUTTONDOWN and is_over(m_pos, (x, y), (wd, ht)):
                    for i, data in enumerate(board_size):
                        if data[0]:
                            data[0] = False
                            break

                    idx = board_size.index(btn)
                    board_size[idx][0] = True

        redraw_options()
        pygame.display.update()
    
    pygame.quit()
    quit()


menu_loop()