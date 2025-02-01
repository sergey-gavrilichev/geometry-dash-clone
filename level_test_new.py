import os
import sys
import pygame
import level_selector


from menu import SCREEN_SIZE


all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(SCREEN_SIZE)


# спрайт игрока
class Player(pygame.sprite.Sprite):
    cube_image = pygame.image.load(os.path.join('assets', 'level_test', 'cube.png'))
    cube_image = pygame.transform.scale(cube_image, (70, 70))
    ship_image = pygame.image.load(os.path.join('assets', 'level_test', 'ship.png'))
    ship_image = pygame.transform.scale(ship_image, (90, 70))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.cube_image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 433
        self.mask = pygame.mask.from_surface(self.image)
        self.jump = 0
        self.jumping = False
        self.falling = False
        self.player_mode = 'cube'
        self.go_up = False
        self.on_block = False

    def update(self, *event):
        # физика для куба
        if self.player_mode == 'cube':
            if event and event[0].type == pygame.MOUSEBUTTONDOWN and self.falling is False and self.jumping is False:
                self.jumping = True
                self.jump = self.rect.y - 124

            # если не на блоке - падаем
            if not self.on_block and not self.jumping:
                self.falling = True

            # прыжок вверх
            if self.jumping:
                if self.rect.y == self.jump:
                    self.jumping = False
                    self.falling = True
                    self.jump = 0
                else:
                    self.rect.y -= 4

            # падение вниз
            if self.falling:
                if self.rect.y >= 433:
                    self.falling = False
                else:
                    self.rect.y += 4

            # сбрасываем переменную стояния на блоке
            self.on_block = False

        else:
            # физика для кораблика
            if pygame.mouse.get_pressed()[0]:
                self.go_up = True
            else:
                self.go_up = False

            if self.go_up and self.rect.y >= 4:
                self.rect.y -= 4
            if self.go_up is False and self.rect.y <= 429:
                self.rect.y += 4


# спрайт орба
class Orb(pygame.sprite.Sprite):
    orb_image = pygame.image.load(os.path.join('assets', 'level_test', 'orb.png'))
    orb_image = pygame.transform.scale(orb_image, (30, 30))

    def __init__(self, x=None, y=None):
        super().__init__(all_sprites)
        self.image = Orb.orb_image
        self.rect = self.image.get_rect()
        self.rect.x = x or 1280
        self.rect.y = y or 383
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -30:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, player):
            player.jump = 301
            player.jumping = True
            player.falling = False
            self.kill()


# спрайты порталов
class PortalCube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        image = pygame.image.load(os.path.join('assets', 'level_test', 'portal_cube.png'))
        self.image = pygame.transform.scale(image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 130
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -85:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, player):
            player.player_mode = 'cube'
            player.image = player.cube_image


class PortalShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        image = pygame.image.load(os.path.join('assets', 'level_test', 'portal_ship.png'))
        self.image = pygame.transform.scale(image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 130
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -85:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, player):
            player.player_mode = 'ship'
            player.image = player.ship_image


# спрайт блока
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
        if pygame.sprite.collide_mask(self, player):
            side = check_collision_side(player, self)
            if side == 'top':
                if player.player_mode == 'cube':
                    player.jumping = False
                    player.falling = False
                    player.on_block = True
                else:
                    player.rect.y -= 4
            if side == 'bottom':
                if player.player_mode == 'cube':
                    cube_crashed(screen)
                else:
                    player.rect.y += 4
            if side == 'horizontal':
                cube_crashed(screen)


# спрайт шипа
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
        if pygame.sprite.collide_mask(self, player):
            cube_crashed(screen)


player = Player()


def check_collision_side(player, block):
    # Определяет сторону столкновения player с block
    dx = (player.rect.centerx - block.rect.centerx)
    dy = (player.rect.centery - block.rect.centery)

    # Найдём размеры пересечения
    intersection = player.rect.clip(block.rect)
    if intersection.width > intersection.height:
        # Вертикальное столкновение
        if dy < 0:
            return "top"
        else:
            return "bottom"
    else:
        # Горизонтальное столкновение
        return "horizontal"


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')

    all_sprites = pygame.sprite.Group()
    player.player_mode = 'cube'
    player.image = player.cube_image
    player.rect.y = 433
    player.jumping = False
    player.falling = False
    all_sprites.add(player)

    # загрузка заднего фона
    background_image = pygame.image.load(os.path.join('assets', 'level_test', 'background.png'))

    # музыка
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('assets', 'level_test', 'music.mp3'))
    pygame.mixer.music.play(-1)

    # ограничение кадров
    clock = pygame.time.Clock()

    # генерация уровня
    with open('level_test.txt', mode='r', encoding='utf8') as readed_file:
        text = readed_file.read().split()[-1]

    x = 1280
    y = 433
    level_dict = {'E': None, 'B': Block, 'S': Spike, 'O': Orb, 'P': PortalCube, 'p': PortalShip}
    flag = False
    height = 1

    for symbol in text:
        # если символ - число, то поднимаем следующий объект
        try:
            symbol = int(symbol)
            y = 433 - 70 * (symbol - 1)
            flag = True
            height = symbol
            continue
        except ValueError:
            # иначе, спавним объект
            object = level_dict.get(symbol)
            if object:
                all_sprites.add(object(x, y))
            if flag:
                y += 70
                height -= 1
                if height == 1:
                    flag = False
                continue
            x += 70
            y = 433

    # основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
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

        # если остался только куб - то уровень закончился и это победа
        if len(all_sprites) == 1:
            level_completed(screen)


# выход в меню выбора уровня
def level_exit():
    pygame.mixer.music.load(os.path.join('assets', 'menu', 'music.mp3'))
    pygame.mixer.music.play(-1)
    level_selector.main()


# куб разбился
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


# куб разбился
def level_completed(level_screen):
    # останавливаем музыку и звук победы
    sound_effect = pygame.mixer.Sound(os.path.join('assets', 'level_test', 'win.mp3'))
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
    text1 = font.render("Вы победили!!!", True, (100, 255, 100))
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
