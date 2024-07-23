from typing import Tuple
from __future__ import annotations


def number_to_words(n):
    """
    Convert a number into its word components in Russian
    """
    if n == 0:
        return 'ноль'

    units = ['', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    teens = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать',
             'семнадцать', 'восемнадцать', 'девятнадцать']
    tens = ['', 'десять', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят',
            'девяносто']
    hundreds = ['', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']

    thousand_units = ['тысяча', 'тысячи', 'тысяч']
    million_units = ['миллион', 'миллиона', 'миллионов']
    billion_units = ['миллиард', 'миллиарда', 'миллиардов']

    words = []

    # Helper function to resolve the correct form of thousands, millions, and billions
    def russian_plural(number, units):
        if number % 10 == 1 and number % 100 != 11:
            return units[0]
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return units[1]
        else:
            return units[2]

    # Helper function to handle numbers below 1000
    def under_thousand(number):
        if number == 0:
            return []
        elif number < 10:
            return [units[number]]
        elif number < 20:
            return [teens[number - 10]]
        elif number < 100:
            return [tens[number // 10], units[number % 10]]
        else:
            return [hundreds[number // 100]] + under_thousand(number % 100)

    # Break the number into the billions, millions, thousands, and the rest
    billions = n // 1_000_000_000
    millions = (n % 1_000_000_000) // 1_000_000
    thousands = (n % 1_000_000) // 1_000
    remainder = n % 1_000

    if billions:
        words += under_thousand(billions) + [russian_plural(billions, billion_units)]
    if millions:
        words += under_thousand(millions) + [russian_plural(millions, million_units)]
    if thousands:
        # Special case for 'one' and 'two' in thousands
        if thousands % 10 == 1 and thousands % 100 != 11:
            words.append('одна')
        elif thousands % 10 == 2 and thousands % 100 != 12:
            words.append('две')
        else:
            words += under_thousand(thousands)
        words.append(russian_plural(thousands, thousand_units))
    words += under_thousand(remainder)

    return ' '.join(word for word in words if word)


def inflect_with_num(
    number: int, forms: Tuple[str, str, str]
) -> str:
    """
    1. Для единицы (1).
    2. Единица 0, от 5 до 9 и от 10 до 20 включительно.
    3. Единицы от 2 до 4 включительно.

    :param number: Число, предшествующее слову
    :param forms: Три заданные формы исчисляемого слова
    :return:
    """

    units = number % 10
    tens = number % 100 - units
    if tens == 10 or units >= 5 or units == 0:
        needed_form = 1
    elif units > 1:
        needed_form = 2
    else:
        needed_form = 0
    return forms[needed_form]