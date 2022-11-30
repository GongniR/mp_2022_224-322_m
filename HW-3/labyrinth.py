import numpy as np
import math
import random

class Labyrinth:
    def __init__(self, height: int, width:  int):

        self.height = height
        self.width = width

        self.draw_item_wall = "⬛"
        self.draw_item_void = "⬜"
        # map
        self.start_point = []
        self.finish_point = []
        self.map_labyrinth = []

        self.__create_labyrinth()

    def draw_labyrinth(self):
        for height in self.map_labyrinth:
            for item in height:
                if not item:
                    print(self.draw_item_wall, end="")
                else:
                    print(self.draw_item_void, end="")
            print("")

    def __create_labyrinth(self):
        """Генерация лабиринта"""
        reach_matrix = []
        for i in range(self.height):  # создаём матрицу достижимости ячеек
            reach_matrix.append([])
            for j in range(self.width):
                reach_matrix[i].append(False)
        transition_matrix = []
        for i in range(self.height * 2 - 1):  # заполнение матрицы переходов
            transition_matrix.append([])
            for j in range(self.width * 2 - 1):
                if i % 2 == 0 and j % 2 == 0:
                    transition_matrix[i].append(True)
                else:
                    transition_matrix[i].append(False)
        self.__start_point_generate(self.height, self.width)
        self.__finish_point_generate(self.height, self.width)
        list_transition = [self.start_point]
        x, y = self.start_point
        reach_matrix[x][y] = True
        x, y, tx, ty = self.__transition_choice(x, y, reach_matrix)
        for i in range(1, self.width * self.height):
            while not (x >= 0 and y >= 0):
                x, y = list_transition[-1]
                list_transition.pop()
                x, y, tx, ty = self.__transition_choice(x, y, reach_matrix)
            reach_matrix[x][y] = True
            list_transition.append((x, y))
            transition_matrix[tx][ty] = True
            x, y, tx, ty = self.__transition_choice(x, y, reach_matrix)
            self.map_labyrinth = transition_matrix

    def __start_point_generate(self, height: int, width:  int):
        """Функция выбора точки начала лабиринта"""
        if random.choice([True, False]):
            if random.choice([True, False]):
                point_start = (0, random.randint(0, width - 1))
            else:
                point_start = (height - 1, random.randint(0, width - 1))
        else:
            if random.choice([True, False]):
                point_start = (random.randint(0, height - 1), 0)
            else:
                point_start = (random.randint(0, height - 1), width - 1)
        self.start_point = point_start

    def __finish_point_generate(self, height: int, width:  int):
        """Выбор точки конца лабиринта"""
        self.finish_point = [ height - 1 - self.start_point[0], width - 1 - self.start_point[1]]

    def __transition_choice(self, x, y, rm):
        """Функция выбора дальнейшего пути в генерации лабиринта"""
        choice_list = []
        if x > 0:
            if not rm[x - 1][y]:
                choice_list.append((x - 1, y))
        if x < len(rm) - 1:
            if not rm[x + 1][y]:
                choice_list.append((x + 1, y))
        if y > 0:
            if not rm[x][y - 1]:
                choice_list.append((x, y - 1))
        if y < len(rm[0]) - 1:
            if not rm[x][y + 1]:
                choice_list.append((x, y + 1))
        if choice_list:
            nx, ny = random.choice(choice_list)
            if x == nx:
                if ny > y:
                    tx, ty = x * 2, ny * 2 - 1
                else:
                    tx, ty = x * 2, ny * 2 + 1
            else:
                if nx > x:
                    tx, ty = nx * 2 - 1, y * 2
                else:
                    tx, ty = nx * 2 + 1, y * 2
            return nx, ny, tx, ty
        else:
            return -1, -1, -1, -1


test = Labyrinth(10, 10)
test.draw_labyrinth()
print()