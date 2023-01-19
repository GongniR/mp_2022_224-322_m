import prettytable
from prettytable import PrettyTable

ta = PrettyTable()
ta.field_names = ["Фамилия", "Имя", "Возраст", "ЗП"]
ta.add_rows(
    [
        ["Иванов", "Иван", 19, 50000],
        ["Петров", "Пётр", 27, 120000],
        ["Сидоров", "Ян", 16, 100],
    ]
)
ta.set_style(prettytable.DEFAULT)
ta.top_junction_char = '■'
ta.bottom_junction_char = '■'
ta.horizontal_char = '■'
ta.vertical_char = '■'
print(ta)
