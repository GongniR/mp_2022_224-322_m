for i in range(0, 16):
    for j in range(0, 16):
        print("\033[38;5;{};48;5;{}m".format(i, j) + "%15s" % "{}:{} \033[0m".format(i, j), end = '')
    print()