import sys
import pygame
import level_selector


from menu import SCREEN_SIZE


def level_exit():
    # выход из уровня после нажатия Esc
    pygame.mixer.music.load('assets//gd_menu_music.mp3')
    pygame.mixer.music.play(-1)
    level_selector.main()


def cube_crashed(screen):
    # останавливаем музыку
    pygame.mixer.music.stop()

    # текст о смерти(
    font = pygame.font.Font(None, 72)
    text_1 = font.render('Вы разбились. Нажмите ЛКМ, чтобы начать снова,', 1, pygame.Color('Red'))
    text_2 = font.render('или ESC, чтобы выйти из уровня.', 1, pygame.Color('Red'))
    screen.blit(text_1, (10, 10))
    screen.blit(text_2, (10, 60))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # новая попытка
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                running = False
                main()
            # выход из уровня + возвращаем музыку из главного меню
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                level_exit()


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # загрузка кубика
    cube_image = pygame.image.load('assets//gd_level_test_cube.png')
    cube_image = pygame.transform.scale(cube_image, (70, 70))

    # музыка
    pygame.mixer.init()
    pygame.mixer.music.load('assets//gd_level_test_music.mp3')
    pygame.mixer.music.play(-1)

    # спавн новых стенок
    walls = []
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 3000)

    def spawn_wall():
        walls.append(1280)

    # настройки для куба
    cube_height = 650
    cube_coords_x = range(70, 140)
    jumping = False
    falling = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                level_exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not falling:
                jumping = True
            elif event.type == spawn_event:
                spawn_wall()

        # прыжок вверх
        if jumping:
            cube_height -= 1
            if cube_height == 500:
                jumping = False
                falling = True

        # падение вниз
        if falling:
            cube_height += 0.5
            if cube_height == 650:
                falling = False

        # передвижение стенок + проверка на столкновение
        for i, wall in enumerate(walls):
            if wall in cube_coords_x and cube_height >= 580:
                running = False
                cube_crashed(screen)
            wall -= 1
            if wall < 0:
                walls.pop(i)
            else:
                walls[i] = wall

        # отрисовка
        screen.fill(pygame.Color('black'))
        screen.blit(cube_image, (70, cube_height))
        for wall in walls:
            pygame.draw.rect(screen, pygame.Color('Red'), (wall, 650, 50, 70))

        pygame.display.flip()
