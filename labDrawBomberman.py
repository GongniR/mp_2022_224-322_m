from random import randint as rd

void_cell = " "
wall_cell = "■"
box = "⧈"

def add_wall(map_array: list) -> list:
    for number_row in range(len(map_array)):
        if number_row == 0 or number_row == len(map_array)-1:
            map_array[number_row] = [wall_cell for i in range(len(map_array[number_row]))]
        else:
            map_array[number_row][0] =  wall_cell
            map_array[number_row][-1] = wall_cell
            if number_row%2 == 0 and number_row >1 and number_row<len(map_array)-2:
                for number_column in range(0, len(map_array[number_row])-1, 2):
                    map_array[number_row][number_column] = wall_cell

    return map_array

def add_box(map_array: list, count_box = 10)->list:

    if count_box>106:
        return add_box(map_array, 106)

    rand_x =  lambda : rd(0, 20)
    rand_y =  lambda : rd(0,8)
    
    while count_box > 0:
        row = rand_y()
        column = rand_x()
        if map_array[row][column] == void_cell:
            map_array[row][column] = box  
            count_box-=1   
    return map_array


def create_map(height = 9, width = 21, box_count = 10) -> list:

    map_array =  [[void_cell for j in range(width) ] for i in range(height)]
    map_array = add_wall(map_array)
    map_array = add_box(map_array,box_count)

    return map_array
test_map = create_map()

def draw_map()->None:
    map_array = create_map()
    for line in map_array:
        for elem in line:
            print(elem, end=" ")
        print("")


draw_map()