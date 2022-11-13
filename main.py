"""
Жиляев Антон ИУ7-14Б

"""
from typing import List, Dict

from curvetools import CurveSeg, integrate_approx, integrate
from iotools import get_number, display_table
from settings import func, antideriv, runs, approximation_methods, exact_method, diff_labels


def read_params() -> tuple[float, float, List[int]]:
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
    integral_approx_method_value = {}
    for approx_method in approximation_methods:
        integral_approx_method_value[approx_method] = \
            [integrate_approx(curve_seg, n_i, approximation_methods[approx_method]) for n_i in n]

    return integral_approx_method_value


def compute_integral_exact(curve_seg: CurveSeg) -> Dict[str, List[float]]:
    integral_exact = {exact_method: [integrate(curve_seg)]}
    return integral_exact


def compute_differences(integrals_approx: Dict[str, List[float]],
                        integral_exact: Dict[str, List[float]]) -> Dict[str, List[float]]:
    integrals_diffs = {}
    for integral in integrals_approx:
        integrals_diffs[f'{integral} {diff_labels["abs"]}'] = [(integ_approx - integral_exact[exact_method][0])
                                                               for integ_approx
                                                               in integrals_approx[integral]]

        integrals_diffs[f'{integral} {diff_labels["rel"]}'] = [(integ_diff_abs / integral_exact[exact_method][0])
                                                               for integ_diff_abs
                                                               in integrals_diffs[f'{integral} {diff_labels["abs"]}']]

    return integrals_diffs


def find_method_max_diff(integrals_approx: Dict[str, List[float]], integrals_diffs: Dict[str, List[float]]) -> str:
    rel_max_diff = 0
    method_max_diff = ''
    for integral in integrals_approx:
        if integrals_diffs[f'{integral} {diff_labels["rel"]}'][-1] > rel_max_diff:
            rel_max_diff = integrals_diffs[f'{integral} {diff_labels["rel"]}'][-1]
            method_max_diff = f'{integral}'

    return method_max_diff


def compute_ndivisions(curve_seg: CurveSeg, method_max_diff: str, eps: float) -> (int, float):
    n = 1
    current_integral_value = integrate_approx(curve_seg, n, approximation_methods[method_max_diff])
    while abs(current_integral_value -
              (next_integral_value := integrate_approx(curve_seg, n * 2, approximation_methods[method_max_diff]))
              ) > eps:
        n *= 2
        current_integral_value = next_integral_value

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
    display_table(table_first, runs)
    display_table(table_second, 1)
