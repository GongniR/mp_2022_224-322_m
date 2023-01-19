def draw_rect(h: int, w: int, fill = False ) -> None: 
    """Отрисовка прямоугольника размером h x w"""
    blok = "██"

    # проверка на нулевой размер значение
    if h == 0 or w == 0:
        return 
    
    # отрисовка 
    for i in range(h):
        for j in range(w):
            # заливка  
            if fill:
                    print(blok, end="")
            else:
                if i == 0 or j == 0 or i == h-1 or  j == w-1:
                    print(blok, end="")
                else:
                    print(" ", end=" ")
        print()
    


# повтор 
check = True
while check:
    again = input("Повторить?[y/n]").lower() == "y"
    if again:
        try:
            H = int(input("Введите высоту:"))
            W = int(input("Введите ширину:"))
            fill_check = input("Закрасить [Y/N] ").lower()== "y"
            draw_rect(H, W, fill_check)
        except:
            print("Вы ввели не число")
            check = False
        