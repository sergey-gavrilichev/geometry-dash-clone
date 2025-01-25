import os
import sys
import pygame
import level_selector


from menu import SCREEN_SIZE, WIDTH, HEIGHT


def level_exit():
    # выход из уровня после нажатия Esc
    pygame.mixer.music.load(os.path.join('assets', 'gd_menu_music.mp3'))
    pygame.mixer.music.play(-1)
    level_selector.main()


def cube_crashed(screen):
    # останавливаем музыку
    pygame.mixer.music.stop()

    # текст о смерти( в окне
    # загрузка заднего фона
    info_background_image = pygame.image.load(os.path.join('assets', 'gd_info.png'))
    info_background_image = pygame.transform.scale(info_background_image, (550, 350))

    # загрузка кнопки "ок"
    ok_button_image = pygame.image.load(os.path.join('assets', 'gd_button_ok.png'))
    ok_button_image = pygame.transform.scale(ok_button_image, (130, 60))

    # отображение окна информации
    screen.blit(info_background_image, (370, 200))
    screen.blit(ok_button_image, (585, 450))

    # отображение текста
    font = pygame.font.Font(None, 50)
    text1 = font.render("Вы разбились.", True, (100, 255, 100))
    text2 = font.render("Для новой игры нажмите", True, (100, 255, 100))
    text3 = font.render("левую кнопку мыши. Для", True, (100, 255, 100))
    text4 = font.render("выхода из уровня - Esc.", True, (100, 255, 100))
    text5 = font.render("Удачи!", True, (100, 255, 100))
    screen.blit(text1, (530, 230))
    screen.blit(text2, (420, 270))
    screen.blit(text3, (420, 310))
    screen.blit(text4, (420, 350))
    screen.blit(text5, (585, 390))
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
    cube_image = pygame.image.load(os.path.join('assets', 'gd_level_test_cube.png'))
    cube_image = pygame.transform.scale(cube_image, (70, 70))

    # музыка
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('assets', 'gd_level_test_music.mp3'))
    pygame.mixer.music.play(-1)

    # спавн новых стенок и треугольников
    flag_spawn = True
    walls = []
    triangles = []
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 3000)

    def spawn_wall():
        walls.append(WIDTH)

    def spawn_triangle():
        triangles.append(WIDTH)

    # настройки для куба
    cube_height = 70
    cube_coords_x = range(70, 140)
    cube_coord_y = 280
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
                if flag_spawn:
                    spawn_wall()
                    flag_spawn = False
                else:
                    spawn_triangle()
                    flag_spawn = True

        # прыжок вверх
        if jumping:
            cube_coord_y -= 1
            if cube_coord_y + cube_coord_y == 200:
                jumping = False
                falling = True

        # падение вниз
        if falling:
            cube_coord_y += 0.5
            if cube_height + cube_coord_y == 350:
                falling = False

        # передвижение стенок + проверка на столкновение
        for i, wall in enumerate(walls):
            if wall in cube_coords_x and cube_height + cube_coord_y >= 280:
                running = False
                cube_crashed(screen)
            wall -= 1
            if wall < 0:
                walls.pop(i)
            else:
                walls[i] = wall

        # передвижение треугольников + проверка на столкновение
        for i, triangle in enumerate(triangles):
            if triangle in cube_coords_x and cube_height + cube_coord_y >= 280:
                running = False
                cube_crashed(screen)
            triangle -= 1
            if triangle < 0:
                triangles.pop(i)
            else:
                triangles[i] = triangle

        # отрисовка
        screen.fill(pygame.Color('black'))
        screen.blit(cube_image, (70, cube_height + cube_coord_y))
        pygame.draw.rect(screen, (100, 255, 100), (0, 420, WIDTH, HEIGHT))
        for wall in walls:
            pygame.draw.rect(screen, pygame.Color('Red'), (wall, 350, 50, 70))
        for triangle in triangles:
            pygame.draw.polygon(screen, pygame.Color('Blue'),
                                [(triangle, 420), (triangle + 25, 350), (triangle + 50, 420)])

        pygame.display.flip()