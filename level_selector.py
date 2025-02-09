import os
import sys
import pygame
import menu
import info
import level


from menu import SCREEN_SIZE, WIDTH, HEIGHT


all_sprites = pygame.sprite.Group()
ok_button_group = pygame.sprite.Group()
go_to_left_dict = {1: 3, 2: 1, 3: 2}
go_to_right_dict = {1: 2, 2: 3, 3: 1}
current_level = 1

do_show_info = False


# спрайт кнопки начала уровня
class StartButton(pygame.sprite.Sprite):
    image_1 = pygame.image.load(os.path.join('assets', 'level_selector', 'play_button_1.png'))
    image_2 = pygame.image.load(os.path.join('assets', 'level_selector', 'play_button_2.png'))
    image_3 = pygame.image.load(os.path.join('assets', 'level_selector', 'play_button_3.png'))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = StartButton.image_1
        self.rect = self.image.get_rect()
        self.rect.x = 220
        self.rect.y = 105

    def update(self, *args):
        # стартуем уровень
        if args and self.rect.collidepoint(args[0].pos):
            sound_effect = pygame.mixer.Sound(os.path.join('assets', 'level_selector', 'play_sound.mp3'))
            pygame.mixer_music.stop()
            sound_effect.play()
            pygame.time.wait(1200)
            global current_level
            if current_level == 1:
                file = 'background_blue.jpg'
                cur_level = 'level_1.txt'
            elif current_level == 2:
                file = 'background_green.jpg'
                cur_level = 'level_2.txt'
            else:
                file = 'background_red.jpg'
                cur_level = 'level_3.txt'
            level.main(file, cur_level)


start_button = StartButton()
start_button_dict = {1: StartButton.image_1, 2: StartButton.image_2, 3: StartButton.image_3}


# спрайт кнопки назад
class BackButton(pygame.sprite.Sprite):
    back_button_image = pygame.image.load(os.path.join('assets', 'gd_button_back.png'))
    back_button_image = pygame.transform.scale(back_button_image, (WIDTH * 0.08, HEIGHT * 0.15))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = BackButton.back_button_image
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 25

    def update(self, *args):
        # возврат в главное меню, если нажата кнопка
        if args and self.rect.collidepoint(args[0].pos):
            menu.main()


# спрайт кнопки информация
class InfoButton(pygame.sprite.Sprite):
    info_button_image = pygame.image.load(os.path.join('assets', 'gd_button_info.png'))
    info_button_image = pygame.transform.scale(info_button_image, (WIDTH * 0.08, HEIGHT * 0.15))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = InfoButton.info_button_image
        self.rect = self.image.get_rect()
        self.rect.x = 1150
        self.rect.y = 25

    def update(self, *args):
        # открытие окна информации, если нажата кнопка
        if args and self.rect.collidepoint(args[0].pos):
            global do_show_info
            do_show_info = True


# спрайт кнопки пролистывания влево
class LeftButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((40, 100), pygame.SRCALPHA, 32)
        pygame.draw.polygon(self.image, pygame.Color('White'), ((0, 50), (40, 0), (40, 100)))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 325

    def update(self, *args):
        # пролистывание влево, если нажата кнопка
        if args and self.rect.collidepoint(args[0].pos):
            global current_level
            current_level = go_to_left_dict.get(current_level)
            start_button.image = start_button_dict.get(current_level)


# спрайт кнопки пролистывания вправо
class RightButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((40, 100), pygame.SRCALPHA, 32)
        pygame.draw.polygon(self.image, pygame.Color('White'), ((40, 50), (0, 0), (0, 100)))
        self.rect = self.image.get_rect()
        self.rect.x = 1220
        self.rect.y = 325

    def update(self, *args):
        # пролистывание вправо, если нажата кнопка
        if args and self.rect.collidepoint(args[0].pos):
            global current_level
            current_level = go_to_right_dict.get(current_level)
            start_button.image = start_button_dict.get(current_level)


# спрайт кнопки "ок"
class OkButton(pygame.sprite.Sprite):
    ok_button_image = pygame.image.load(os.path.join('assets', 'gd_button_ok.png'))
    ok_button_image = pygame.transform.scale(ok_button_image, (130, 60))

    def __init__(self):
        super().__init__(ok_button_group)
        self.image = OkButton.ok_button_image
        self.rect = self.image.get_rect()
        self.rect.x = 585
        self.rect.y = 450

    def update(self, *event):
        if event and self.rect.collidepoint(event[0].pos):
            global do_show_info
            do_show_info = False


# добавляем спрайты в группу
all_sprites.add(BackButton())
all_sprites.add(InfoButton())
all_sprites.add(LeftButton())
all_sprites.add(RightButton())
all_sprites.add(start_button)

ok_button_group.add(OkButton())


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # загрузка заднего фона
    background_image_1 = pygame.image.load(os.path.join('assets', 'level_selector', 'background_1.png'))
    background_image_2 = pygame.image.load(os.path.join('assets', 'level_selector', 'background_2.png'))
    background_image_3 = pygame.image.load(os.path.join('assets', 'level_selector', 'background_3.png'))

    # основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                all_sprites.update(event, screen)
                ok_button_group.update(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu.main()

        # отображение
        global current_level
        if current_level == 1:
            screen.blit(background_image_1, (0, 0))
        elif current_level == 2:
            screen.blit(background_image_2, (0, 0))
        else:
            screen.blit(background_image_3, (0, 0))

        all_sprites.draw(screen)

        # отображение информации, если нужно
        global do_show_info
        if do_show_info:
            info.main(screen)
            ok_button_group.draw(screen)

        pygame.display.flip()

    pygame.quit()
