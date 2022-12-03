"""
Шаблоны для задания кривых и функции их обработки
"""


from typing import Callable


class Curve:
    """
    Класс, который описывает кривую по функции и её первообразной первого порядка
    """
    def __init__(self, function: Callable, antiderivative: Callable):
        self.func = function
        self.antideriv = antiderivative


class CurveSeg(Curve):
    """
    Класс, который уточняет сегмент кривой по её левой и правой границы
    """
    def __init__(self, function: Callable, antiderivative: Callable, left_bound: float, right_bound: float):
        super().__init__(function, antiderivative)
        self.left_bound = left_bound
        self.right_bound = right_bound


def integrate(curve_seg: CurveSeg) -> float:
    """
    Вычисляет площадь по графиком кривой
    :param curve_seg:
    :return:
    """
    return curve_seg.antideriv(x=curve_seg.right_bound) - curve_seg.antideriv(x=curve_seg.left_bound)


def integrate_approx(curve_seg: CurveSeg, steps: int, height_computation: Callable) -> float:
    average_height = 0
    step_size = (curve_seg.right_bound - curve_seg.left_bound) / steps

    pos_left, pos_right = curve_seg.left_bound, None
    for i in range(steps):
        pos_right = curve_seg.left_bound + step_size * (i + 1)
        average_height += height_computation(left=pos_left, right=pos_right, sample_height=curve_seg.func)

        pos_left = pos_right

    area = average_height / steps * (curve_seg.right_bound - curve_seg.left_bound)
    return area
