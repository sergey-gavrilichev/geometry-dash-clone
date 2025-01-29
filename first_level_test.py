import os
import sys
import pygame
from level_test_new import Cube, SCREEN_SIZE, level_exit

all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(SCREEN_SIZE)

cube = Cube()


class Block(pygame.sprite.Sprite):
    block_image = pygame.image.load(os.path.join('assets', 'level_test', 'block.png'))
    block_image = pygame.transform.scale(block_image, (70, 70))

    def __init__(self, x=None, y=None):
        super().__init__(all_sprites)
        self.image = Block.block_image
        self.rect = self.image.get_rect()
        self.rect.x = x or 1280
        self.rect.y = y or 433
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -70:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, cube) == (65, 0):
            cube.falling = True
        elif pygame.sprite.collide_mask(self, cube):
            if cube.rect.y <= 365:
                cube.falling = False
            else:
                cube_crashed(screen)


class Spike(pygame.sprite.Sprite):
    spike_image = pygame.image.load(os.path.join('assets', 'level_test', 'spike.png'))
    spike_image = pygame.transform.scale(spike_image, (70, 70))

    def __init__(self, x=None, y=None):
        super().__init__(all_sprites)
        self.image = Spike.spike_image
        self.rect = self.image.get_rect()
        self.rect.x = x or 1280
        self.rect.y = y or 433
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -70:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, cube):
            cube_crashed(screen)


def main():
    # читаем из файла препятствия
    with open(os.path.join('levels', 'first_level_barriers.txt'), encoding='utf8') as f:
        barriers = f.read().split()

    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    all_sprites = pygame.sprite.Group()
    all_sprites.add(cube)

    # загрузка заднего фона
    background_image = pygame.image.load(os.path.join('assets', 'level_test', 'background.png'))

    # музыка
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('assets', 'level_test', 'music.mp3'))
    pygame.mixer.music.play(-1)

    # ограничение кадров
    clock = pygame.time.Clock()

    # спавн шипов
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 6000)

    # спавн препятствий
    def spawn(spawn_flag):
        if spawn_flag == '1':
            all_sprites.add(Block())
        elif spawn_flag == '2':
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
                if len(barriers) > 1:
                    spawn_flag = barriers[0]
                    del barriers[0]
                    spawn(spawn_flag)
                elif len(all_sprites) == 1:
                    win(screen)
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


def win(screen):
    # загрузка заднего фона
    info_background_image = pygame.image.load(os.path.join('assets', 'gd_info.png'))
    info_background_image = pygame.transform.scale(info_background_image, (550, 350))

    # загрузка кнопки "ок"
    ok_button_image = pygame.image.load(os.path.join('assets', 'gd_button_ok.png'))
    ok_button_image = pygame.transform.scale(ok_button_image, (130, 60))

    # отображение окна информации
    screen.blit(info_background_image, (370, 200))
    screen.blit(ok_button_image, (585, 450))

    # отображение текста
    font = pygame.font.Font(None, 50)
    text1 = font.render("Вы выиграли!", True, (100, 255, 100))
    text2 = font.render("Для новой игры нажмите", True, (100, 255, 100))
    text3 = font.render("левую кнопку мыши. Для", True, (100, 255, 100))
    text4 = font.render("выхода из уровня - Esc.", True, (100, 255, 100))
    text5 = font.render("Удачи!", True, (100, 255, 100))
    screen.blit(text1, (530, 230))
    screen.blit(text2, (420, 270))
    screen.blit(text3, (420, 310))
    screen.blit(text4, (420, 350))
    screen.blit(text5, (585, 390))
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


def cube_crashed(level_screen):
    # останавливаем музыку и звук смерти
    pygame.mixer.music.stop()
    sound_effect = pygame.mixer.Sound(os.path.join('assets', 'level_test', 'death_sound.mp3'))
    sound_effect.play()

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


if __name__ == '__main__':
    main()
