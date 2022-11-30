import numpy as np 

def draw_snail(h: int, w: int) -> None: 
    # отрисовка улитки
    blok = "██"
    plot = create_snail(h, w)
    for iy in range(h):
        for ix in range(w):
            if plot[iy][ix] == blok:
                print(blok, end="")
            else:
                print(" ", end=" ")
            
        print()

def get_array(h: int, w: int) -> None:
    # лист для отрисовки улитки 
    plot_list = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append(" ")
        plot_list.append(row) 
    return plot_list

def create_snail(h: int, w: int) -> list:
    # формирование узора улитки 
    blok = "██"
    plot = get_array(h, w)
    i = 0
    y = 0
    x = 0
    while not plot[y][x] == '':
        check_x = x
        check_y = y
        while x < w - 1 - 2 * i:
            plot[y][x] = blok
            x+=1
        while y < h - 1 - 2 * i:
            plot[y][x] = blok
            y+=1
        while x > 0 + 2 * i:
            plot[y][x] = blok
            x-=1
        while y > 2 + 2 * i:
            plot[y][x] = blok
            y-=1
        i += 1
        if check_x == x:
            if check_y == y:
                break
    return plot

# приме
draw_snail(12,11)

