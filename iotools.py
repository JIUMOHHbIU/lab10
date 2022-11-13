from typing import Callable, Any, List, Dict

from settings import format_out_number, name_width, runs, separetor_vr, separetor_hr, separetor_cross


def get_number(convert_function: Callable, prompt='') -> Any:
    """
    Запрашивает на вход число, пока пользователь не введет корректные данные

    :param convert_function: функция перевода ввода в число в нужной форме
    :param prompt: приглашение ко вводу для пользователя
    :return: объект, возращенный convert_function от введенной пользователем строки
    """

    value = None
    while value is None:
        input_string = input(prompt)
        try:
            value = convert_function(input_string)
        except ValueError:
            print('Полученная строка не является валидным числом')

    return value


def str_border(columns):
    return f'{separetor_hr * (len(str_dict({"": [0]*columns})) - 1)}\n'


def str_named_list(name: str, values: List) -> str:
    name = f'{name:<{name_width}}'
    values = f'{f" {separetor_vr} ".join([f"{element:{format_out_number}}" for element in values])}'
    content = name + f' {separetor_vr} ' + values
    return f'{separetor_vr} ' + content + f' {separetor_vr}' + '\n'


def str_dict(dictionary: Dict) -> str:
    s = ''
    for key in dictionary:
        s += str_named_list(key, dictionary[key])
    return s


def form_output_block(dictionary: Dict[str, List[float]], columns) -> str:
    block = (str_dict(dictionary)) + str_border(columns)
    return block


def replace_cross_separetors(table: str) -> str:
    table = list(table.split('\n'))

    for i in range(1, len(table)):
        new_line = ''

        for j in range(min(len(table[i]), len(table[i - 1]))):
            if table[i - 1][j] == separetor_vr and table[i][j] == separetor_hr:
                new_line += separetor_cross
            else:
                new_line += table[i][j]
        for j in range(min(len(table[i]), len(table[i - 1])), len(table[i])):
            new_line += table[i][j]

        table[i] = new_line

    for i in range(len(table) - 1):
        new_line = ''

        for j in range(min(len(table[i]), len(table[i + 1]))):
            if table[i + 1][j] == separetor_vr and table[i][j] == separetor_hr:
                new_line += separetor_cross
            else:
                new_line += table[i][j]
        for j in range(min(len(table[i]), len(table[i + 1])), len(table[i])):
            new_line += table[i][j]

        table[i] = new_line

    table = '\n'.join(table)
    return table


def display_table(dictionaries: List[Dict[str, List[float]]], columns: int) -> None:
    table = str_border(columns)
    for dictionary in dictionaries:
        table += form_output_block(dictionary, columns)

    table = replace_cross_separetors(table)
    print(table)
