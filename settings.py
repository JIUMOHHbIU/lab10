from math import cos, sin
from typing import Any, Callable

format_out_number = '>12.5g'
runs = 2
name_width = 80
separetor_vr = '║'
separetor_hr = '═'
separetor_cross = '╬'
exact_method = 'Через первообразную'
diff_labels = {
    'abs': 'абсолютная погрешность',
    'rel': 'относительная погрешность',
}


def height_middle_rect(left: float, right: float, sample_height: Callable):
    return sample_height(x=(left + right) / 2)


def height_parabol(left: float, right: float, sample_height: Callable):
    return (sample_height(x=left)
            + 4 * sample_height(x=(left + right) / 2)
            + sample_height(x=right)) / 6


def func(**kwargs: [str, Any]) -> float:
    x = kwargs['x']

    return x - cos(x)


def antideriv(**kwargs: [str, Any]) -> float:
    x = kwargs['x']

    return x**2/2 - sin(x)


approximation_methods = {
    'Срединные прямоугольники': height_middle_rect,
    'Параболы': height_parabol,
}
