import random
import sys

import pygame

from map import Map


# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Моя PyGame Игра")

# Цвета
PLAYER_COLOR = (97, 175, 239)
TEXT_COLOR = (220, 220, 220)

# Игрок
player_size = 8
player_speed = 3

# Шрифт
font = pygame.font.SysFont(None, 36)

# Частота кадров
clock = pygame.time.Clock()
FPS = 60

# Карта
TILE_SIZE = 8
# Рассчитываем размер карты, чтобы заполнить весь экран
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
map_generator = Map(MAP_WIDTH, MAP_HEIGHT)


def generate_new_map():
    global cave_map, player_x, player_y

    # Генерация новой карты
    mini_map = map_generator.generate_cave()
    cave_map = map_generator.upscale_map(
        mini_map, multiplication_factor=3
    )  # Уже не увеличиваем, так как размер рассчитан

    # Находим все проходимые клетки (пол)
    floor_positions = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if cave_map[y][x] == 0:
                floor_positions.append(
                    (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                )

    # Выбираем случайную позицию для игрока
    if floor_positions:
        player_x, player_y = random.choice(floor_positions)


# Генерируем первую карту и позицию игрока
generate_new_map()

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                generate_new_map()  # Генерация новой карты при нажатии SPACE

    # Обработка управления (клавиши движения)
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[pygame.K_a]:
        new_x -= player_speed
    if keys[pygame.K_d]:
        new_x += player_speed
    if keys[pygame.K_w]:
        new_y -= player_speed
    if keys[pygame.K_s]:
        new_y += player_speed

    # Проверка коллизий
    new_rect = pygame.Rect(
        new_x - player_size // 2, new_y - player_size // 2, player_size, player_size
    )
    can_move = True

    # Проверяем, не выходит ли игрок за границы экрана
    if (
        new_rect.left < 0
        or new_rect.right > SCREEN_WIDTH
        or new_rect.top < 0
        or new_rect.bottom > SCREEN_HEIGHT
    ):
        can_move = False
    else:
        # Проверяем столкновение со стенами
        for y in range(
            max(0, new_rect.top // TILE_SIZE), min(MAP_HEIGHT, (new_rect.bottom // TILE_SIZE) + 1)
        ):
            for x in range(
                max(0, new_rect.left // TILE_SIZE),
                min(MAP_WIDTH, (new_rect.right // TILE_SIZE) + 1),
            ):
                if cave_map[y][x] == 1:  # Если это стена
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if new_rect.colliderect(tile_rect):
                        can_move = False
                        break
            if not can_move:
                break

    if can_move:
        player_x, player_y = new_x, new_y

    # Отрисовка
    screen.fill((0, 0, 0))  # Очистка экрана

    # Отрисовка карты
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if cave_map[y][x] == 1:
                pygame.draw.rect(screen, (30, 30, 50), rect)  # Стена
            else:
                pygame.draw.rect(screen, (70, 70, 100), rect)  # Пол
            # Рисуем сетку
            pygame.draw.rect(screen, (20, 20, 30), rect, 1)

    # Отрисовка игрока (центрируем)
    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        (player_x - player_size // 2, player_y - player_size // 2, player_size, player_size),
    )

    # Отображение инструкции
    font = pygame.font.SysFont(None, 24)
    text = font.render("Нажмите SPACE для новой карты, ESC для выхода", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

pygame.quit()
sys.exit()
