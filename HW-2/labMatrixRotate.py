import random

MATRIX = []

def fill_matrix(h: int, w: int ):
    '''заполнение матрицы рандомными числами'''
    for _ in range(h):
        row = []
        for _ in range(w):
            row.append(random.randint(10, 99))
        MATRIX.append(row)

def draw_matrix(h: int, w: int):
    '''отрисовка матрицы'''
    for y in range(h):
        for x in range(w):
            print(MATRIX[x][y], end=' ')
        print()


def turn_left():
    '''поворот налево'''
    global MATRIX
    h, w = len(MATRIX), len(MATRIX[0])
    new_array = [[None] * h for _ in range(w)]
    for c in range(w - 1, -1, -1):
        for r in range(h):
            new_array[c][h - r - 1] = MATRIX[r][c]
    MATRIX = new_array.copy()


def turn_right():
    '''поворот направо'''
    global MATRIX
    h, w = len(MATRIX), len(MATRIX[0])
    new_array = [[None] * h for _ in range(w)]
    for c in range(w):
        for r in range(h - 1, -1, -1):
            new_array[w - c - 1][r] = MATRIX[r][c]
    MATRIX = new_array.copy()


def flip():
    '''отражение матрицы '''
    global MATRIX
    h, w = len(MATRIX), len(MATRIX[0])
    new_array = [[None] * h for _ in range(w)]
    for c in range(w):
        for r in range(h):
            new_array[r][c] = MATRIX[w - r - 1][c]
    MATRIX = new_array.copy()



def init_matrix_and_command() -> None:
    try:
        h = int(input("Введите высоту матрицы: "))
        w = int(input("Введите ширину матрицы: "))
    except ValueError:
        return
    fill_matrix(h, w)
    draw_matrix(h, w)
    while True:
        command = input("Введите команду ").lower()

        if command == 'a':
            turn_left()
            draw_matrix(h, w)
        elif command == 'd':
            turn_right()
            draw_matrix(h, w)
        elif command == 's':
            flip()
            draw_matrix(h, w)

init_matrix_and_command()