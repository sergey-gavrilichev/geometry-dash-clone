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

    # отображение текста
    font = pygame.font.Font(None, 50)
    text1 = font.render("Как играть?", True, (100, 255, 100))
    text2 = font.render("Для прыжка нажимайте", True, (100, 255, 100))
    text3 = font.render("левую кнопку мыши. Для", True, (100, 255, 100))
    text4 = font.render("выхода из уровня - Esc.", True, (100, 255, 100))
    text5 = font.render("Удачи!", True, (100, 255, 100))
    screen.blit(text1, (550, 230))
    screen.blit(text2, (420, 270))
    screen.blit(text3, (420, 310))
    screen.blit(text4, (420, 350))
    screen.blit(text5, (585, 390))

