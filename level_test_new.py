import os
import sys
import pygame
import level_selector


from menu import SCREEN_SIZE


all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(SCREEN_SIZE)


# спрайт кубика
class Cube(pygame.sprite.Sprite):
    cube_image = pygame.image.load(os.path.join('assets', 'gd_level_test_cube.png'))
    cube_image = pygame.transform.scale(cube_image, (70, 70))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Cube.cube_image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 433
        self.mask = pygame.mask.from_surface(self.image)
        self.jumping = False
        self.falling = False

    def update(self, *event):
        if event and event[0].type == pygame.MOUSEBUTTONDOWN and not self.falling:
            self.jumping = True

        # прыжок вверх
        if self.jumping:
            self.rect.y -= 4
            if self.rect.y == 333:
                self.jumping = False
                self.falling = True

        # падение вниз
        if self.falling:
            self.rect.y += 2
            if self.rect.y == 433:
                self.falling = False


# спрайт шипа
class Spike(pygame.sprite.Sprite):
    spike_image = pygame.image.load(os.path.join('assets', 'gd_level_test_spike.png'))
    spike_image = pygame.transform.scale(spike_image, (70, 70))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Spike.spike_image
        self.rect = self.image.get_rect()
        self.rect.x = 1280
        self.rect.y = 433
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -70:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, cube):
            cube_crashed(screen)


cube = Cube()


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')

    # добавляем спрайты в группу
    all_sprites = pygame.sprite.Group()
    all_sprites.add(Spike())
    all_sprites.add(cube)

    # загрузка заднего фона
    background_image = pygame.image.load(os.path.join('assets', 'gd_level_test_background.png'))

    # музыка
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('assets', 'gd_level_test_music.mp3'))
    pygame.mixer.music.play(-1)

    # ограничение кадров
    clock = pygame.time.Clock()

    # спавн шипов
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 3000)

    def spawn_spike():
        all_sprites.add(Spike())

    # основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
            elif event.type == spawn_event:
                spawn_spike()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                level_exit()

        # отрисовка
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

        # обновление спрайтов
        all_sprites.update()

        # ограничение кадров
        clock.tick(60)


# выход в меню выбора уровня
def level_exit():
    pygame.mixer.music.load(os.path.join('assets', 'gd_menu_music.mp3'))
    pygame.mixer.music.play(-1)
    level_selector.main()


# куб разбился
def cube_crashed(level_screen):
    # останавливаем музыку
    pygame.mixer.music.stop()

    # загрузка заднего фона
    info_background_image = pygame.image.load(os.path.join('assets', 'gd_info.png'))
    info_background_image = pygame.transform.scale(info_background_image, (550, 350))

    # загрузка кнопки "ок"
    ok_button_image = pygame.image.load(os.path.join('assets', 'gd_button_ok.png'))
    ok_button_image = pygame.transform.scale(ok_button_image, (130, 60))

    # отображение окна информации
    level_screen.blit(info_background_image, (370, 200))
    level_screen.blit(ok_button_image, (585, 450))

    # отображение текста
    font = pygame.font.Font(None, 50)
    text1 = font.render("Вы разбились.", True, (100, 255, 100))
    text2 = font.render("Для новой игры нажмите", True, (100, 255, 100))
    text3 = font.render("левую кнопку мыши. Для", True, (100, 255, 100))
    text4 = font.render("выхода из уровня - Esc.", True, (100, 255, 100))
    text5 = font.render("Удачи!", True, (100, 255, 100))
    level_screen.blit(text1, (530, 230))
    level_screen.blit(text2, (420, 270))
    level_screen.blit(text3, (420, 310))
    level_screen.blit(text4, (420, 350))
    level_screen.blit(text5, (585, 390))
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
