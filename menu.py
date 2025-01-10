import sys
import pygame
import level_selector


SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # загрузка заднего фона
    background_image = pygame.image.load('assets//gd_menu_background.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # загрузка лого
    logo_image = pygame.image.load('assets//gd_menu_logo.png')
    logo_image = pygame.transform.scale(logo_image, (WIDTH * 0.6, HEIGHT * 0.3))

    # загрузка кнопки "играть"
    play_button_image = pygame.image.load('assets//gd_menu_play_button.png')
    play_button_image = pygame.transform.scale(play_button_image, (300, 300))
    play_button_borders_x = range(495, 795)
    play_button_borders_y = range(300, 600)

    # основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # открытие меню выбора уровня если нажата кнопка
                condition_1 = event.pos[0] in play_button_borders_x
                condition_2 = event.pos[1] in play_button_borders_y
                if condition_1 and condition_2:
                    level_selector.main()
                    running = False

        # отображение
        screen.blit(background_image, (0, 0))
        screen.blit(logo_image, (250, 35))
        screen.blit(play_button_image, (495, 300))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    # загрузка и воспроизведение музыки. переместил, чтобы не начиналось с начала
    pygame.mixer.init()
    pygame.mixer.music.load('assets//gd_menu_music.mp3')
    pygame.mixer.music.play(-1)

    main()
