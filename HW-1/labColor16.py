"""<Вывод цветов 16>"""
for i in range(30, 38):
    for j in range(40, 48):
        print("\033[0;{};{}m {}:{} \033[0m".format(j, i, i, j), end="")
    
    print()