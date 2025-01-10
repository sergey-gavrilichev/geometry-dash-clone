import sys
import pygame
import menu
import info
import level_test


from menu import SCREEN_SIZE, WIDTH, HEIGHT


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)
    flag_info = False

    # переменные для перелистывания
    go_to_left_dict = {1: 3, 2: 1, 3: 2}
    go_to_right_dict = {1: 2, 2: 3, 3: 1}
    current_level = 1

    # загрузка заднего фона
    background_image = pygame.image.load('assets//gd_level_selector_background.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # загрузка кнопки "назад"
    back_button_image = pygame.image.load('assets//gd_button_back.png')
    back_button_image = pygame.transform.scale(back_button_image, (WIDTH * 0.08, HEIGHT * 0.15))
    back_button_borders_x = range(25, 128)
    back_button_borders_y = range(25, 133)

    # закгрузка кнопки "информация"
    info_button_image = pygame.image.load('assets//gd_button_info.png')
    info_button_image = pygame.transform.scale(info_button_image, (WIDTH * 0.08, HEIGHT * 0.15))
    info_button_borders_x = range(1150, 1253)
    info_button_borders_y = range(25, 133)

    ok_button_borders_x = range(585, 715)
    ok_button_borders_y = range(450, 510)

    # кнопки влево и вправо для пролистывания уровней
    left_button_borders_x = range(20, 60)
    left_button_borders_y = range(325, 425)
    right_button_borders_x = range(1220, 1260)
    right_button_borders_y = range(325, 425)

    # границы для кнопки старта
    start_button_borders_x = range(300, 980)
    start_button_borders_y = range(175, 425)

    # текст
    font = pygame.font.Font(None, 72)
    text_level_1 = font.render('Первый уровень', 1, pygame.Color('White'))
    text_level_2 = font.render('Второй уровень', 1, pygame.Color('White'))
    text_level_3 = font.render('Третий уровень', 1, pygame.Color('White'))

    # основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not flag_info:
                    # открытие главного меню, если нажата кнопка "назад"
                    if event.pos[0] in back_button_borders_x and event.pos[1] in back_button_borders_y:
                        menu.main()
                        running = False
                    # открытие окна информации, если нажата кнопка "информация"
                    elif event.pos[0] in info_button_borders_x and event.pos[1] in info_button_borders_y:
                        flag_info = True
                    # пролистывание уровней
                    elif event.pos[0] in left_button_borders_x and event.pos[1] in left_button_borders_y:
                        current_level = go_to_left_dict.get(current_level)
                    elif event.pos[0] in right_button_borders_x and event.pos[1] in right_button_borders_y:
                        current_level = go_to_right_dict.get(current_level)
                    # открытие уровня. пока что все открывают один и тот же тестовый уровень
                    elif event.pos[0] in start_button_borders_x and event.pos[1] in start_button_borders_y:
                        level_test.main()
                        running = False
                else:
                    # закрытие окна информации, если нажата кнопка "ок"
                    if event.pos[0] in ok_button_borders_x and event.pos[1] in ok_button_borders_y:
                        flag_info = False

        # отображение
        screen.blit(background_image, (0, 0))
        screen.blit(back_button_image, (25, 25))
        screen.blit(info_button_image, (1150, 25))

        # рисуем стрелки влево и вправо
        pygame.draw.polygon(screen, pygame.Color('White'),((20, 375), (60, 325), (60, 425)))
        pygame.draw.polygon(screen, pygame.Color('White'),((1260, 375), (1220, 325), (1220, 425)))

        # отображение поля с текущем уровнем
        pygame.draw.rect(screen, pygame.Color('Grey'), (300, 175, 680, 250))
        pygame.draw.rect(screen, pygame.Color('Grey'), (300, 450, 680, 50))

        if current_level == 1:
            screen.blit(text_level_1, (440, 225))
        elif current_level == 2:
            screen.blit(text_level_2, (440, 225))
        else:
            screen.blit(text_level_3, (440, 225))

        # отображение окна информации
        if flag_info:
            info.main(screen)

        pygame.display.flip()

    pygame.quit()
