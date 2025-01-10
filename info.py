import pygame


def main(screen):
    # загрузка заднего фона
    info_background_image = pygame.image.load('assets//gd_info.png')
    info_background_image = pygame.transform.scale(info_background_image, (550, 350))

    # загрузка кнопки "ок"
    ok_button_image = pygame.image.load('assets//gd_button_ok.png')
    ok_button_image = pygame.transform.scale(ok_button_image, (130, 60))

    # отображение окна информации
    screen.blit(info_background_image, (370, 200))
    screen.blit(ok_button_image, (585, 450))
