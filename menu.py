import os
import sys
import pygame
import level_selector


SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720
all_sprites = pygame.sprite.Group()


# спрайт кнопки перехода к выбору уровня
class PlayButton(pygame.sprite.Sprite):
    play_button_image = pygame.image.load(os.path.join('assets', 'menu', 'play_button.png'))
    play_button_image = pygame.transform.scale(play_button_image, (270, 270))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = PlayButton.play_button_image
        self.rect = self.image.get_rect()
        self.rect.x = 505
        self.rect.y = 175

    def update(self, *event):
        # открывем меню выбора уровня, если была нажата кнопка
        if event and self.rect.collidepoint(event[0].pos):
            level_selector.main()


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # ставим иконку игре
    pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'gd_icon.png')))

    # добавляем play_button в группу all_sprites
    all_sprites.add(PlayButton())

    # загрузка заднего фона
    background_image = pygame.image.load(os.path.join('assets', 'menu', 'background.png'))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                all_sprites.update(event)

        # отображение
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    # загрузка и воспроизведение музыки
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('assets', 'menu', 'music.mp3'))
    pygame.mixer.music.play(-1)

    main()
