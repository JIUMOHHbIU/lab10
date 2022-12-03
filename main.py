"""
Жиляев Антон ИУ7-14Б
Программа находит площадь под графиком кривой, заданной пользователем
"""
from typing import List, Dict

from curvetools import CurveSeg, integrate_approx, integrate
from iotools import get_number, display_table
from settings import func, antideriv, runs, approximation_methods, exact_method, diff_labels


def read_params() -> tuple[float, float, List[int]]:
    """
    Обрабатывает ввод параметров интегрирования

    :return: Параметры интегрирования
    """
    left_bound = get_number(float, 'Введите левую границу интегрирования: ')
    while (right_bound := get_number(float, 'Введите правую границу интегрирования: ')) <= left_bound:
        print('Правая граница должна быть больше левой границы')
    n = []
    for i in range(runs):
        while (n_i := get_number(int, f'Введите количество участков интегрирования N{i + 1}: ')) < 1:
            print('Количество участков интегрирования должно быть больше 0')
        n += [n_i]
    return left_bound, right_bound, n


def compute_integrals_approximations(curve_seg: CurveSeg, n: List[int]) -> Dict[str, List[float]]:
    """
    Вычисляет площадь под графиком кривой через глобально заданные методы численного интегрирования

    :param curve_seg: Объект, содержащий все данные о свойствах кривой
    :param n: Список количеств сегментов интегрирования
    :return: Словарь с указание метода и вычисленными площадями для соответствующих разбиений
    """
    integral_approx_method_value = {}
    for approx_method in approximation_methods:
        integral_approx_method_value[approx_method] = \
            [integrate_approx(curve_seg, n_i, approximation_methods[approx_method]) for n_i in n]

    return integral_approx_method_value


def compute_integral_exact(curve_seg: CurveSeg) -> Dict[str, List[float]]:
    """
    Вычисляет площадь под графиком кривой через первообразную функции

    :param curve_seg: Объект, содержащий все данные о свойствах кривой
    :return: Словарь с указание метода и вычисленными площадями для соответствующих разбиений
    """
    integral_exact = {exact_method: [integrate(curve_seg)]}
    return integral_exact


def compute_differences(integrals_approx: Dict[str, List[float]],
                        integral_exact: Dict[str, List[float]]) -> Dict[str, List[float]]:
    """
    Вычисляет относительную и абсолютную погрешность методов численного интегрирования

    :param integrals_approx: Словарь со списками значений для каждого количества участков разбиения с доступом по названию метода приближения
    :param integral_exact: Точное значение интеграла
    :return: Словарь с указанием погрешностей для каждого метода и соответствующего количества участков разбиения
    """
    integrals_diffs = {}
    for integral in integrals_approx:
        integrals_diffs[f'{integral} {diff_labels["abs"]}'] = [abs(integ_approx - integral_exact[exact_method][0])
                                                               for integ_approx
                                                               in integrals_approx[integral]]

        integrals_diffs[f'{integral} {diff_labels["rel"]}'] = [(integ_diff_abs / integral_exact[exact_method][0])
                                                               for integ_diff_abs
                                                               in integrals_diffs[f'{integral} {diff_labels["abs"]}']]

    return integrals_diffs


def find_method_max_diff(integrals_approx: Dict[str, List[float]], integrals_diffs: Dict[str, List[float]]) -> str:
    """
    Находит метод с самым большим отклонением при одном из указанных форматов разбиения

    :param integrals_approx: Словарь со списками значений для каждого количества участков разбиения с доступом по названию метода приближения
    :param integrals_diffs: Словарь со списками погрешностей для каждого количества участков разбиения с доступом по названию метода приближения
    :return:
    """
    abs_max_diff = -1
    method_max_diff = ''
    for integral in integrals_approx:
        if integrals_diffs[f'{integral} {diff_labels["rel"]}'][-1] > abs_max_diff:
            abs_max_diff = integrals_diffs[f'{integral} {diff_labels["rel"]}'][-1]
            method_max_diff = f'{integral}'

    return method_max_diff


def compute_ndivisions(curve_seg: CurveSeg, method_max_diff: str, eps: float) -> (int, float):
    """
    Находит достаточное количество участков разбиения для достижения требуемой точности

    :param curve_seg: Объект, содержащий все данные о свойствах кривой
    :param method_max_diff: Название неэффективного метода
    :param eps: Заданная точность
    :return: Необходимое число участков разбиения
    """
    n = 1
    current_integral_value = integrate_approx(curve_seg, n, approximation_methods[method_max_diff])
    while abs(current_integral_value -
              (next_integral_value := integrate_approx(curve_seg, n * 2, approximation_methods[method_max_diff]))
              ) > eps:
        n *= 2
        current_integral_value = next_integral_value
    print(current_integral_value - next_integral_value)
    return n, next_integral_value


def main():
    # Ввод
    left_bound, right_bound, n = read_params()

    # Вычисление
    curve_seg = CurveSeg(func, antideriv, left_bound, right_bound)
    integrals_approx = compute_integrals_approximations(curve_seg, n)
    integral_exact = compute_integral_exact(curve_seg)
    integrals_diffs = compute_differences(integrals_approx, integral_exact)

    # Нахождение худшего метода
    method_max_diff = find_method_max_diff(integrals_approx, integrals_diffs)

    # Ввод числа eps
    while (eps := get_number(float, 'Введите ожидаемую точность: ')) <= 0:
        print('Точность должна быть положительной')

    # Нахождение достаточного количества участков разбиения
    ndivisions, integ_value = compute_ndivisions(curve_seg, method_max_diff, eps)
    integral_to_eps = {f'{method_max_diff}, количество участков: {ndivisions}': [integ_value]}
    integral_to_eps_diffs = compute_differences(integral_to_eps, integral_exact)

    # Вывод
    header_dict = {
        'Метод/Количество участков интегрирования': [n_i for n_i in n],
    }

    table_first = [
        header_dict,
        integrals_approx,
        integrals_diffs,
    ]
    table_second = [
        integral_exact,
        integral_to_eps,
        integral_to_eps_diffs,
    ]

    print()
    display_table(table_first, columns=runs)
    display_table(table_second, columns=1)
