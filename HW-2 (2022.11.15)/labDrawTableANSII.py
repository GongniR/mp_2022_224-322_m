def draw_table() -> None: 
    # отрисовка таблицы 
    for i in range(32,128):
        print("%4d-%s" % (i,chr(i)), end='')
        if i%10 == 0:
            print()
            
# пример запуска 
draw_table()