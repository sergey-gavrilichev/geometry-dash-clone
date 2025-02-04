import os
import pygame


def main(screen):
    # загрузка заднего фона
    info_background_image = pygame.image.load(os.path.join('assets', 'gd_info.png'))
    info_background_image = pygame.transform.scale(info_background_image, (550, 350))

    # текст
    font = pygame.font.Font(None, 50)
    texts = [
        "Как играть?",
        "Для прыжка нажимайте",
        "левую кнопку мыши. Для",
        "выхода из уровня - Esc.",
        "Удачи!"
    ]

    rendered_texts = [font.render(text, True, (100, 255, 100)) for text in texts]

    # отображение окна информации
    screen.blit(info_background_image, (370, 200))

    # отображение текста
    x_position = 420
    y_position = 230
    line_height = 40
    for i, rendered_text in enumerate(rendered_texts):
        screen.blit(rendered_text, (x_position, y_position + i * line_height))
