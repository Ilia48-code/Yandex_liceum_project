import pygame
import sys
import time
import random
import pygameMenu

# Мы можем изменять скорость игры
# Легко      ->  10
# Средне   ->  25
# Сложно    ->  40
# Очень сложно    ->  60
# Невозможно ->  120
difficulty = 25

# Размеры окна
frame_size_x = 720
frame_size_y = 480

# Проверка на ошибки, хз зачем мне так посоветовали сделать(придумал не сам)
check_errors = pygame.init()

if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} Ошибка при запуске игры , подождите ...')
    sys.exit(-1)
else:
    print('Игра запущена ')

# Инициализация окна
pygame.display.set_caption('Змейка на pygame')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Инициализация  (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Колличество FPS
fps_controller = pygame.time.Clock()

# Сама игра
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Конец игры
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Счёт
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)
    pygame.display.flip()


# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Определение нажатия кнопки
        elif event.type == pygame.KEYDOWN:
            # W -> Вверх; S -> Вниз; A -> Влево; D -> Вправо
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Выход из игры
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Проверка, что змейка не может двигаться назад
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Передвижение змейки
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Отрисовка змейки
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Спавн еды для змейки
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True

    # Графика
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Еда змейки
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Конец игры
    # Ограничение выхода за пределы поля
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()
    # Определение врезания
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    # Обновление экрана
    pygame.display.update()
    # Частота обновления кадров
    fps_controller.tick(difficulty)
