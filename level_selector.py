import pygame
import menu


SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720
GO_TO_LEFT_DICT = {1: 3, 2: 1, 3: 2}
GO_TO_RIGHT_DICT = {1: 2, 2: 3, 3: 1}
current_level = 1


# пролистывание уровней влево
def go_to_left():
    global current_level
    current_level = GO_TO_LEFT_DICT.get(current_level)

# пролистывание уровней вправо
def go_to_right():
    global current_level
    current_level = GO_TO_RIGHT_DICT.get(current_level)


# вернуться в главное меню
def back_to_menu():
    menu.main()
    pygame.quit()


def main():
    pygame.init()
    pygame.display.set_caption('Geometry Dash Clone')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    left_button_borders_x = range(20, 60)
    left_button_borders_y = range(325, 425)

    right_button_borders_x = range(1220, 1260)
    right_button_borders_y = range(325, 425)

    back_to_menu_button_borders_x = range(20, 60)
    back_to_menu_button_borders_y = range(20, 90)

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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_x, click_y = event.pos[0], event.pos[1]
                if click_x in left_button_borders_x and click_y in left_button_borders_y:
                    go_to_left()
                elif click_x in right_button_borders_x and click_y in right_button_borders_y:
                    go_to_right()
                elif click_x in back_to_menu_button_borders_x and click_y in back_to_menu_button_borders_y:
                    back_to_menu()

        # красим фон и рисуем стрелки
        screen.fill(pygame.Color('Blue'))
        pygame.draw.polygon(screen, pygame.Color('White'),((20, 375), (60, 325), (60, 425)))
        pygame.draw.polygon(screen, pygame.Color('White'),((1260, 375), (1220, 325), (1220, 425)))
        pygame.draw.polygon(screen, pygame.Color('Green'),((20, 55), (60, 20), (60, 90)))

        # отображаем кнопку для текущего уровня
        pygame.draw.rect(screen, pygame.Color('Grey'), (300, 175, 680, 250))
        pygame.draw.rect(screen, pygame.Color('Grey'), (300, 450, 680, 50))
        global current_level
        if current_level == 1:
            screen.blit(text_level_1, (440, 225))
        elif current_level == 2:
            screen.blit(text_level_2, (440, 225))
        else:
            screen.blit(text_level_3, (440, 225))
        pygame.display.flip()

    pygame.quit()
