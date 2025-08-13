import random
import numpy as np


class Map:
    def __init__(
        self,
        width: int,
        height: int,
    ):
        """
        Параметры:
        width, height - размеры карты
        """
        self.width = width
        self.height = height

    def count_neighbors(self, grid, x: int, y: int):
        """Функция для подсчета соседних стен."""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx, ny = x + i, y + j
                if i == 0 and j == 0:
                    continue
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    count += grid[ny][nx]
                else:
                    count += 1  # Края карты считаем стенами
        return count

    def generate_cave(
        self,
        fill_prob: float = 0.4,
        smooth_steps: int = 5,
        birth_limit: int = 4,
        death_limit: int = 3,
    ):
        """
        Генерация пещеры с помощью клеточного автомата

        Параметры:
        fill_prob - вероятность заполнения клетки стеной (0.0-1.0)
        smooth_steps - количество итераций сглаживания
        birth_limit - сколько соседей нужно для "рождения" стены
        death_limit - сколько соседей нужно для "смерти" стены

        Возвращает 2D массив, где:
        0 - проходимая клетка (пол)
        1 - стена
        """
        # Создаем случайную начальную карту
        map = np.zeros((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < fill_prob:
                    map[y][x] = 1

        # Применяем сглаживание
        for _ in range(smooth_steps):
            new_map = map.copy()
            for y in range(self.height):
                for x in range(self.width):
                    neighbors = self.count_neighbors(map, x, y)

                    # Правила преобразования
                    if map[y][x] == 1:
                        if neighbors < death_limit:
                            new_map[y][x] = 0
                    else:
                        if neighbors > birth_limit:
                            new_map[y][x] = 1
            map = new_map

        # Обеспечиваем проходимые границы
        map[0, :] = 1  # Верхняя граница
        map[-1, :] = 1  # Нижняя граница
        map[:, 0] = 1  # Левая граница
        map[:, -1] = 1  # Правая граница

        return map

    def upscale_map(self, original_map, multiplication_factor: int = 3):
        """
        Увеличивает карту в multiplication_factor раз, сохраняя пропорции

        Параметры:
        original_map - исходная карта (2D numpy array)
        multiplication_factor - во сколько раз умножим размер карты

        Возвращает:
        Увеличенную карту (2D numpy array)
        """
        # Получаем новые размеры
        new_height = self.height * multiplication_factor
        new_width = self.width * multiplication_factor

        # Создаем новую увеличенную карту
        upscaled_map = np.zeros((new_height, new_width))

        for y in range(self.height):
            for x in range(self.width):
                # Получаем значение из оригинальной карты
                tile_value = original_map[y][x]

                # Определяем область в увеличенной карте
                start_y = y * multiplication_factor
                end_y = start_y + multiplication_factor
                start_x = x * multiplication_factor
                end_x = start_x + multiplication_factor

                # Заполняем область в увеличенной карте
                upscaled_map[start_y:end_y, start_x:end_x] = tile_value

        return upscaled_map
