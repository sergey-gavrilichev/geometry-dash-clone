import os
import sys
import pygame
import menu
import info
import level_test


from menu import SCREEN_SIZE, WIDTH, HEIGHT


all_sprites = pygame.sprite.Group()
ok_button_group = pygame.sprite.Group()
go_to_left_dict = {1: 3, 2: 1, 3: 2}
go_to_right_dict = {1: 2, 2: 3, 3: 1}
current_level = 1

do_show_info = False


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

# спрайт кнопки начала уровня
class StartButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((680, 250), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('Grey'), (0, 0, 680, 250))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 175

    def update(self, *args):
        # стартуем уровень. пока он один - тестовый
        if args and self.rect.collidepoint(args[0].pos):
            level_test.main()


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
all_sprites.add(StartButton())

ok_button_group.add(OkButton())


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # загрузка заднего фона
    background_image = pygame.image.load(os.path.join('assets', 'gd_level_selector_background.png'))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

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
                all_sprites.update(event, screen)
                ok_button_group.update(event)

        # отображение
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # в будущем - прогресс на уровне
        pygame.draw.rect(screen, pygame.Color('Grey'), (300, 450, 680, 50))

        # отображение текущего уровня
        global current_level
        if current_level == 1:
            screen.blit(text_level_1, (440, 225))
        elif current_level == 2:
            screen.blit(text_level_2, (440, 225))
        else:
            screen.blit(text_level_3, (440, 225))

        # отображение информации, если нужно
        global do_show_info
        if do_show_info:
            info.main(screen)
            ok_button_group.draw(screen)

        pygame.display.flip()

    pygame.quit()
