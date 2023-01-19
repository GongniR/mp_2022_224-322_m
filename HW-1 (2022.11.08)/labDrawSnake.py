def draw_sneak(h: int, w: int) -> None: 
    """Отрисовка змейки размером h x w"""
    blok = "██"

    # проверка на нулевой размер значение
    if h == 0 or w == 0:
        return 
    
    # отрисовка 
    for i in range(h):
        for j in range(w):
            if (i % 2 == 0 or (j == w - 1 and i % 4 == 1) or (j == 0 and i % 4 == 3)):
                print(blok, end="")
            else:
                print(" ", end=" ")
        print()
# отрисовка змейки
draw_sneak(14,13)