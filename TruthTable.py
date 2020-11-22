import itertools
import re


def is_in(symbol: str, _list) -> bool:
    """
    Данная функция смотрит, есть ли символ в списке
    :param symbol: Исходный символ
    :param _list: Список
    :return: Да/Нет
    """

    if len(_list) == 0:
        return False

    for _l in _list:
        for _ in _l:
            if _ == symbol:
                return True
    return False


def create_priorities(_priorities: str) -> dict:
    """
    Данная функция нужна для создания приоритетов
    Сначала идут самые высокие операции, потом ниже.

    :param _priorities: строка с знаками операций.
    Если они разделены запятой, то операция ниже по рангу

    :return: Словарь приоритета операций
    """

    pr = {}
    _prior = _priorities.split(',')
    count = len(_prior) + 1

    for ch in _prior:                           # Проход по всей строке
        if len(ch) == 1:                        # Если в текущем приоритете 1 символ
            if not is_in(ch, pr.values()):
                pr.update({count: list(ch)})
                count -= 1
        elif len(ch) > 1:                       # Если в текущем приоритете больше 1 символа
            a = []
            for c in ch:                        # То пробегаемся по всем им
                if not is_in(c, pr.values()):
                    if c not in a:
                        a.append(c)
            pr.update({count: a})
            count -= 1
    pr.update({count: ['(', ')']})
    return pr


def get_priorities(_operator: str, _priorities: dict) -> int:
    """
    Получаем номер приоритета операции

    :param _operator: Нужный символ
    :param _priorities: Словарь приоритетов
    :return: Номер приоритета
    """

    for num, ch in _priorities.items():
        if _operator in ch:
            return num
    print("Incorrect operator [", _operator, "]! Returned -1.")
    return -1


def remake_to_rev_pol_not(_string: str, _priorities: dict) -> str:
    """
    Фукнция для перевода выражения в обратную польскую запись.
    Возвращает строку.

    :param _string: Исходное выражение
    :param _priorities: Приоритеты операций
    :return: Выражение в ОПЗ
    """

    stack = []
    result_str = ''

    for c in _string:
        if not is_in(c, _priorities.values()):     # Если это не символ операции
            # print(list(c) not in _priorities.values())
            # print(c, " - ", _priorities.values())
            result_str += c                         # То пишем его в исходную строку
        elif c == '(':                              # Если это открывающая скобка
            stack.append(c)                         # То добавляем ее в стек
        elif len(stack) == 0 and c != ')':          # Иначе, это символ операции. Смотрим, пуст ли стек
            stack.append(c)                         # Если да, то добавляем символ без проверки
        elif len(stack) != 0:                       # Если нет, то проверяем Тек > Верх на стеке
            last_in_stack = None if not stack else stack[-1]    # Если нет, то выводим все
            while get_priorities(c, _priorities) <= get_priorities(last_in_stack, _priorities):
                if last_in_stack == '(':
                    break

                result_str += stack.pop()
                last_in_stack = None if not stack else stack[-1]
            if c != ')':
                stack.append(c)
        elif c == ')':                                                  # Если закрывающая скобка, то
            last_in_stack = None if not stack else stack[-1]            # выводим все до открывающей скобки
            while last_in_stack != '(' or last_in_stack is not None:
                result_str += stack.pop()
                last_in_stack = None if not stack else stack[-1]
            stack.pop()

    while len(stack) != 0:                                              # Если после прохода по строке стек
        last_in_stack = None if not stack else stack[-1]                # еще не пуст, то выводим всё, что осталось
        if last_in_stack != '(':
            result_str += stack.pop()
        else:
            stack.pop()

    return result_str


def main():
    source_str = input('Enter boolean expression: ').replace(' ', '')
    priority_str = input('Enter priorities: ')
    p = create_priorities(priority_str)
    print("Priorities: ", p)
    print("Reverse Pol Notation: ", remake_to_rev_pol_not(source_str, p))


if __name__ == '__main__':
    main()
