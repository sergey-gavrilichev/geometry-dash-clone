import pygame
import menu
import info
from menu import SCREEN_SIZE, WIDTH, HEIGHT


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)

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

    # основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # открытие главного меню, если нажата кнопка
                if event.pos[0] in back_button_borders_x and event.pos[1] in back_button_borders_y:
                    menu.main()
                    running = False
                # открытие окна информации, если нажата кнопка
                elif event.pos[0] in info_button_borders_x and event.pos[1] in info_button_borders_y:
                    info.main()

        # отображение
        screen.blit(background_image, (0, 0))
        screen.blit(back_button_image, (25, 25))
        screen.blit(info_button_image, (1150, 25))
        pygame.display.flip()

    pygame.quit()
