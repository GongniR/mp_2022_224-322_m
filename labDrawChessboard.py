def draw_chess()->None:
    """
    Отрисовка шахматной доски
    :return:
    """
    #  элементы для клеток

    black_cell = "⬛"
    white_cell = "⬜"
    #  кол-во строк и линий
    n = 8
    name_cell = "  | a b c d e f g h|  "

    print(name_cell)
    for row in range(1, n+1):
        if row % 2 == 1:
            print(str(row) + " |" + (black_cell+white_cell)*4 + "| " + str(row))
        else:
            print(str(row) + " |" + (white_cell+black_cell)*4 + "| " + str(row))
    print(name_cell)

draw_chess()