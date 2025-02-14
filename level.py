import os
import sys
import pygame
import random
import level_selector


from menu import SCREEN_SIZE

# Инициализация Pygame
pygame.init()

# Основные переменные
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(SCREEN_SIZE)
alpha_surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
cur_level = None


# Спрайт игрока
class Player(pygame.sprite.Sprite):
    cube_image = pygame.image.load(os.path.join('assets', 'level', 'cube.png'))
    cube_image = pygame.transform.scale(cube_image, (70, 70))
    ship_image = pygame.image.load(os.path.join('assets', 'level', 'ship.png'))
    ship_image = pygame.transform.scale(ship_image, (90, 70))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.cube_image
        self.original_image = self.image  # Сохраняем оригинальное изображение
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 433
        self.mask = pygame.mask.from_surface(self.image)
        self.jump = 0
        self.jumping = False
        self.falling = False
        self.is_cube = True
        self.go_up = False
        self.on_block = False
        self.particles = []
        self.rotation = 0  # Угол поворота

    def update(self, *event):
        # Очистка alpha_surf
        alpha_surf.fill((0, 0, 0, 0))
        
        # физика для куба
        if self.is_cube:
            self.original_image = Player.cube_image
            if event and event[0].type == pygame.MOUSEBUTTONDOWN and self.falling is False and self.jumping is False:
                self.jumping = True
                self.jump = self.rect.y - 124

            # если не на блоке - падаем
            if not self.on_block and not self.jumping:
                self.falling = True

            # прыжок вверх
            if self.jumping:
                if self.rect.y == self.jump:
                    self.rotation -= 90  # Плавный поворот
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
            self.original_image = Player.ship_image
            # физика для кораблика
            if pygame.mouse.get_pressed()[0]:
                self.go_up = True
            else:
                self.go_up = False

            if self.go_up and self.rect.y >= 4:
                self.rect.y -= 4
            if self.go_up is False and self.rect.y <= 429:
                self.rect.y += 4

        # Применение поворота к изображению
        self.image = pygame.transform.rotate(self.original_image, self.rotation % 360)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.draw_particle_trail(self.rect.x, self.rect.y)
    
    def draw_particle_trail(self, x, y, color=(255, 255, 255)):
        """Рисует след частиц за игроком"""
        
        self.particles.append([[x + self.rect.width / 2, y + self.rect.height],
                               [random.randint(0, 25) / 10 - 1, random.choice([0, 0])],
                               random.randint(5, 8)])

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.5
            particle[1][0] -= 0.4
            pygame.draw.rect(alpha_surf, color,
                             ([int(particle[0][0]), int(particle[0][1])], [int(particle[2]), int(particle[2])]))
            if particle[2] <= 0:
                self.particles.remove(particle)


# спрайт орба
class Orb(pygame.sprite.Sprite):
    orb_image = pygame.image.load(os.path.join('assets', 'level', 'orb.png'))
    orb_image = pygame.transform.scale(orb_image, (30, 30))

    def __init__(self, file, x=None, y=None):
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
            player.jump = player.rect.y - 124
            player.jumping = True
            player.falling = False
            self.kill()


# спрайты порталов
class PortalCube(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super().__init__(all_sprites)
        image = pygame.image.load(os.path.join('assets', 'level', 'portal_cube.png'))
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
            player.is_cube = True
            player.image = player.cube_image
            player.rotation = 0  # Сброс угла поворота


class PortalShip(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super().__init__(all_sprites)
        image = pygame.image.load(os.path.join('assets', 'level', 'portal_ship.png'))
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
            player.is_cube = False
            player.image = player.ship_image
            player.rotation = 0  # Сброс угла поворота


# спрайт блока
class Block(pygame.sprite.Sprite):
    block_image = pygame.image.load(os.path.join('assets', 'level', 'block.png'))
    block_image = pygame.transform.scale(block_image, (70, 70))

    def __init__(self, file,  x=None, y=None):
        super().__init__(all_sprites)
        self.image = Block.block_image
        self.rect = self.image.get_rect()
        self.rect.x = x or 1280
        self.rect.y = y or 433
        self.mask = pygame.mask.from_surface(self.image)
        self.file = file  # запонимает файл с цветом фона

    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -70:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, player):
            side = check_collision_side(player, self)
            if side == 'top':
                if player.is_cube:
                    player.jumping = False
                    player.falling = False
                    player.on_block = True
                else:
                    player.rect.y -= 4
            if side == 'bottom':
                if player.is_cube:
                    cube_crashed(screen, self.file)
                else:
                    player.rect.y += 4
            if side == 'horizontal':
                cube_crashed(screen, self.file)


# спрайт шипа
class Spike(pygame.sprite.Sprite):
    spike_image = pygame.image.load(os.path.join('assets', 'level', 'spike.png'))
    spike_image = pygame.transform.scale(spike_image, (70, 70))

    def __init__(self, file, x=None, y=None):
        super().__init__(all_sprites)
        self.image = Spike.spike_image
        self.rect = self.image.get_rect()
        self.rect.x = x or 1280
        self.rect.y = y or 433
        self.mask = pygame.mask.from_surface(self.image)
        self.file = file  # запонимает файл с цветом фона

    def update(self, *event):
        # перемещение
        self.rect.x -= 5
        if self.rect.x <= -70:
            self.kill()

        # проверка на столкновение
        if pygame.sprite.collide_mask(self, player):
            cube_crashed(screen, self.file)


# перевёрнутый шип(для верха)
class ReverseSpike(Spike):
    reverse_spike_image = pygame.image.load(os.path.join('assets', 'level', 'reverse_spike.png'))
    reverse_spike_image = pygame.transform.scale(reverse_spike_image, (70, 70))

    def __init__(self, file, x=None, y=None):
        super().__init__(all_sprites)
        self.image = ReverseSpike.reverse_spike_image
        self.rect.x = x or 1280
        self.rect.y = y or 433
        self.file = file


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


def main(file, curr_level):
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')

    all_sprites = pygame.sprite.Group()
    player.is_cube = True
    player.image = player.cube_image
    player.rotation = 0
    player.rect.y = 433
    player.jumping = False
    player.falling = False
    all_sprites.add(player)

    global cur_level
    cur_level = curr_level

    # загрузка заднего фона
    background_image = pygame.image.load(os.path.join('assets', 'level', file))

    # музыка
    if curr_level == 'level_1.txt':
        music = 'music_1.mp3'
    elif curr_level == 'level_2.txt':
        music = 'music_2.mp3'
    else:
        music = 'music_3.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('assets', 'level', music))
    pygame.mixer.music.play(-1)

    # ограничение кадров
    clock = pygame.time.Clock()

    # генерация уровня
    with open(os.path.join('levels', cur_level), mode='r', encoding='utf8') as readed_file:
        text = readed_file.read().split()[-1]

    x = 1280
    y = 433
    level_dict = {'E': None, 'B': Block, 'S': Spike, 'O': Orb, 'P': PortalCube, 'p': PortalShip, 'R': ReverseSpike}
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
                all_sprites.add(object(file, x, y))
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

        # Очистка экрана и alpha_surf
        screen.blit(background_image, (0, 0))
        alpha_surf.fill((0, 0, 0, 0))
        
        # отрисовка
        all_sprites.draw(screen)
        
        # Отображение alpha_surf на экране после всех отрисовок
        screen.blit(alpha_surf, (0, 0))
        pygame.display.flip()

        # обновление спрайтов
        all_sprites.update()

        # ограничение кадров
        clock.tick(60)

        # если остался только куб - то уровень закончился и это победа
        if len(all_sprites) == 1:
            level_completed(screen, file)


# выход в меню выбора уровня
def level_exit():
    pygame.mixer.music.load(os.path.join('assets', 'menu', 'music.mp3'))
    pygame.mixer.music.play(-1)
    level_selector.main()


# куб разбился
def cube_crashed(level_screen, file):
    # останавливаем музыку и звук смерти
    pygame.mixer.music.stop()
    sound_effect = pygame.mixer.Sound(os.path.join('assets', 'level', 'death_sound.mp3'))
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
                global cur_level
                main(file, cur_level)
            # выход из уровня + возвращаем музыку из главного меню
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                level_exit()


# победа
def level_completed(level_screen, file):
    # останавливаем музыку и звук победы
    sound_effect = pygame.mixer.Sound(os.path.join('assets', 'level', 'win.mp3'))
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
                global cur_level
                main(file, cur_level)
            # выход из уровня + возвращаем музыку из главного меню
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                level_exit()
