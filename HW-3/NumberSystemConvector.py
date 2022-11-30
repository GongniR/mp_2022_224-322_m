def convert_number(number_for_convert: str, cc_input=10, cc_output=2) -> int:
    '''
    Перевод числа из заданной системы в новую систему
    '''
    try:
        cc_input = int(cc_input)
        cc_output = int(cc_output)
    except ValueError:
        print("CC должны быть числами!")

    # перевод в 10 сс
    number_for_10_СС = int(str(number_for_convert), cc_input)

    if cc_output == 10:
        return number_for_10_СС
    else:
        # алфавит для перевода в сс
        convert_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if number_for_10_СС < cc_output:
            return convert_alphabet[number_for_10_СС]
        else:
            return convert_number(number_for_10_СС // cc_output, cc_output= cc_output) \
                   + convert_alphabet[number_for_10_СС % cc_output]

while True:

    #  входные данные
    try:
        input_cc = int(input("Введите исходную СС: "))
        output_cc = int(input("Введите новую СС: "))
    except ValueError:
        print("CC должны быть числами!")
    else:
        number = input("Введите число для преобразования: ")
        new_number = convert_number(number, input_cc, output_cc)
        print("Результат: \n" + f"{number}: {input_cc} CC -> {new_number}: {output_cc} CC ")

    again = input("Повторить?[y/n] ").lower() == "n"
    if again:
        break


