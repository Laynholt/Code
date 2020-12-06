from tkinter import *
from PIL import ImageTk
# from PIL import ImageGrab
from PIL import Image as PilImage


class Scheme:
    def __init__(self, parent, width, height, resizable=(False, False), title='Cody', icon=None, scale=75, simple=True):

        _size = (scale, scale)
        self.scale = scale

        self.width = width
        self.height = height

        self.root = Toplevel(parent)
        self.root.geometry(f'{width}x{height}')
        self.root.resizable(resizable[0], resizable[1])
        self.root.title(title)
        if icon is not None:
            self.root.iconbitmap(icon)

        self.wrapper1 = LabelFrame(self.root)

        self.canvas = Canvas(self.wrapper1, width=0.95 * self.width, height=0.9 * self.height)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))

        self.xscrollbar = Scrollbar(self.wrapper1, orient=HORIZONTAL, command=self.canvas.xview)
        self.xscrollbar.grid(column=0, row=1, sticky=(W, E))

        self.yscrollbar = Scrollbar(self.wrapper1, orient=VERTICAL, command=self.canvas.yview)
        self.yscrollbar.grid(column=1, row=0, sticky=(N, S))

        self.canvas.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.main_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor=NW)
        self.wrapper1.pack(fill='both', expand=1, padx=10, pady=10)

        with PilImage.open("resources/or.png").resize(_size, PilImage.ANTIALIAS) as self.img_or:
            pass
        with PilImage.open("resources/and.png").resize(_size, PilImage.ANTIALIAS) as self.img_and:
            pass
        with PilImage.open("resources/xor.png").resize(_size, PilImage.ANTIALIAS) as self.img_xor:
            pass
        with PilImage.open("resources/not.png").resize(_size, PilImage.ANTIALIAS) as self.img_not:
            pass
        with PilImage.open("resources/coder.png").resize(_size, PilImage.ANTIALIAS) as self.img_coder:
            pass
        with PilImage.open("resources/decoder.png").resize(_size, PilImage.ANTIALIAS) as self.img_decoder:
            pass
        with PilImage.open("resources/multi_not.png").resize(_size, PilImage.ANTIALIAS) as self.img_multi_not:
            pass
        with PilImage.open("resources/multi_xor.png").resize(_size, PilImage.ANTIALIAS) as self.img_multi_xor:
            pass
        with PilImage.open("resources/hor_line.png").resize(_size, PilImage.ANTIALIAS) as self.img_hor_line:
            pass
        with PilImage.open("resources/s_top_line.png").resize(_size, PilImage.ANTIALIAS) as self.img_top_corn:
            pass
        with PilImage.open("resources/s_bot_line.png").resize(_size, PilImage.ANTIALIAS) as self.img_bot_corn:
            pass
        with PilImage.open("resources/s_bot_line_deep.png").resize(_size, PilImage.ANTIALIAS) as self.img_bot_deep:
            pass
        with PilImage.open("resources/s_top_line_deep.png").resize(_size, PilImage.ANTIALIAS) as self.img_top_deep:
            pass

        self.rev_pol_not = ['X', '/', 'Y', 'v', 'Z', 'K', '/', 'L', '/', '*', '/', 'v', '/', 'v']
        self._operators = ['/', '*', 'v']

        self.name_of_variable = []  # Переменные в выражении
        self.rows = []  # Все строки, которые будут задействованы в выражении (хранит номер столбца)

        self.stack = []
        self.element_position = {}
        self.count_i, self.count_j = 0, 0

        self.img = []
        self.count_img = 0
        # self.full_img = ''

        self.simple = simple

        if self.simple:
            self.all_img = {'v': self.img_or, '*': self.img_and, '+': self.img_xor, '/': self.img_not,
                            'h': self.img_hor_line, 't1': self.img_top_corn, 'b1': self.img_bot_corn,
                            't2': self.img_top_deep, 'b2': self.img_bot_deep}
        else:
            self.all_img = {'v': self.img_coder, '*': self.img_decoder, '+': self.img_multi_xor,
                            '/': self.img_multi_not,
                            'h': self.img_hor_line, 't1': self.img_top_corn, 'b1': self.img_bot_corn,
                            't2': self.img_top_deep, 'b2': self.img_bot_deep}

    def draw(self, rev_pol_not: list, _operators: list):
        """
        Метод для запуска алгоритма рисования
        :param rev_pol_not: ОПЗ
        :param _operators: операторы
        :return:
        """
        self.rev_pol_not = rev_pol_not
        self._operators = _operators

        self.create_simple_scheme()

    def descent(self, var: str, _need_sum: int, table_of_variable: dict, table_of_actions: dict):
        """
        Метод для разбивки текущего операнда, для изменения его спена
        :param var: текущий операнд
        :param _need_sum: нужный спен
        :param table_of_variable: таблица переменных
        :param table_of_actions: таблица со всеми действиями
        :return:
        """

        if var in self.name_of_variable:
            table_of_variable[var]['rowspan'] = _need_sum
        else:
            v1 = table_of_actions[var]['var'][0]
            v2 = table_of_actions[var]['var'][1]

            if v1 == '':
                self.descent(v2, _need_sum, table_of_variable, table_of_actions)
            elif v2 == '':
                self.descent(v1, _need_sum, table_of_variable, table_of_actions)
            else:
                self.descent(v1, _need_sum // 2, table_of_variable, table_of_actions)
                self.descent(v2, _need_sum // 2, table_of_variable, table_of_actions)

            table_of_actions[var]['rowspan'] = _need_sum

    def analyze_string(self, rev_pol_not: list, _operators: list) -> dict:
        """
        Метод для анализа строки. Нужен, чтобы выделить под каждую переменную нужное количество строк.
        :param rev_pol_not: ОПЗ
        :param _operators: операторы
        :return: таблицу переменных с нужными позициями
        """

        table_of_variables = {}
        table_of_actions = {}
        table_of_variables.update({'_all': {'row': 0, 'col': 0, 'rowspan': 1}})

        stack = []
        count = 0

        for ch in self.rev_pol_not:  # Считаем количество переменных
            if ch not in self._operators:  # А также запоминаем их имена
                self.name_of_variable.append(ch)

        for ch in rev_pol_not:
            if ch not in _operators:
                stack.append(ch)

                table_of_variables.update({ch: {'row': count, 'col': 0, 'rowspan': 1}})
                count += 1
                table_of_variables['_all']['row'] += 1

            else:
                if ch == '/' or ch == '~' and len(stack) != 0:
                    var1 = stack.pop()
                    stack.append(f'{var1}{ch}')

                    _t = table_of_variables[var1] if var1 in self.name_of_variable else table_of_actions[var1]

                    _row = _t['row']
                    _col = _t['col']
                    _rowspan = _t['rowspan']

                    table_of_actions.update({f'{var1}{ch}': {'row': _row, 'col': _col + 1, 'rowspan': _rowspan,
                                                             'var': [var1, '']}})

                elif len(stack) > 1:
                    var1 = stack.pop()
                    var2 = stack.pop()

                    stack.append(f'{var2}{var1}{ch}')

                    _t1 = table_of_variables[var1] if var1 in self.name_of_variable else table_of_actions[var1]
                    _t2 = table_of_variables[var2] if var2 in self.name_of_variable else table_of_actions[var2]

                    _row1 = _t1['row']
                    _col1 = _t1['col']
                    _rowspan1 = _t1['rowspan']

                    _row2 = _t2['row']
                    _col2 = _t2['col']
                    _rowspan2 = _t2['rowspan']

                    _rowspan = max(_rowspan1, _rowspan2)
                    _row = min(_row1, _row2)
                    _col = max(_col1, _col2)

                    if _rowspan1 < _rowspan:
                        self.descent(var1, _rowspan, table_of_variables, table_of_actions)
                    if _rowspan2 < _rowspan:
                        self.descent(var2, _rowspan, table_of_variables, table_of_actions)

                    table_of_actions.update(
                        {f'{var2}{var1}{ch}': {'row': _row, 'col': _col + 1, 'rowspan': 2 * _rowspan,
                                               'var': [var1, var2]}})

        i = _row = _rowspan = 0
        for ch in self.name_of_variable:
            if i != 0:
                table_of_variables[ch]['row'] += i
            i += table_of_variables[ch]['rowspan'] - 1

            if _rowspan < table_of_variables[ch]['rowspan']:
                _rowspan = table_of_variables[ch]['rowspan']
            if _row < table_of_variables[ch]['row']:
                _row = table_of_variables[ch]['row']

        table_of_variables['_all']['rowspan'] = _rowspan
        table_of_variables['_all']['row'] = _row + 1

        return table_of_variables

    def round_rows(self, var1, var2):
        """
        Метод для выравнивания столбцов у операндов путем дорисовывания горизонтальных линий.
        :param var1: первый операнд
        :param var2: второй операнд
        :return:
        """

        _pull_row = _need_col = _pull_col = _pull_span = 0

        if self.element_position[var1]['col'] > self.element_position[var2]['col']:
            _pull_row = self.element_position[var2]['row']
            _pull_col = self.element_position[var2]['col']
            _pull_span = self.element_position[var2]['rowspan']
            _need_col = self.element_position[var1]['col']
        elif self.element_position[var1]['col'] < self.element_position[var2]['col']:
            _pull_row = self.element_position[var1]['row']
            _pull_col = self.element_position[var1]['col']
            _pull_span = self.element_position[var1]['rowspan']
            _need_col = self.element_position[var2]['col']

        while _need_col != _pull_col:
            self.img.append(ImageTk.PhotoImage(self.all_img['h']))
            Label(self.main_frame, image=self.img[self.count_img]).grid(row=_pull_row, column=_pull_col + 1,
                                                                        rowspan=_pull_span, sticky=NS)
            self.rows[_pull_row] += 1  # переходим на след столбец
            self.count_img += 1
            _pull_col += 1

    def create_simple_scheme(self):
        """
        Метод для создания схемы исходного выражения
        :return:
        """

        self.element_position = self.analyze_string(self.rev_pol_not, self._operators)

        for i in range(self.element_position['_all']['row']):
            self.rows.append(0)  # Добавляем новые строки
            # Заполняе строки путыми лейблами, чтобы спены работали
            if self.scale % 75 == 0:
                h = 5 * self.scale // 75
            else:
                h = 3 * self.scale // 50

            Label(self.main_frame, height=h, text='').grid(row=self.count_i, column=self.count_j,
                                                           rowspan=1,
                                                           sticky=NS)
            self.count_i += 1

        for ch in self.rev_pol_not:
            if ch not in self._operators:
                self.stack.append(ch)

                Label(self.main_frame, text=ch).grid(row=self.element_position[ch]['row'], column=0,
                                                     rowspan=self.element_position[ch]['rowspan'], sticky=NS)
                self.rows[self.element_position[ch]['row']] += 1  # переходим на след столбец

            else:
                if ch == '/' or ch == '~' and len(self.stack) != 0:
                    var1 = self.stack.pop()  # Достаем верхний элемент
                    self.stack.append(f'{ch}{var1}')

                    self.img.append(ImageTk.PhotoImage(self.all_img[ch]))

                    self.element_position.update({f'{ch}{var1}': {'row': self.element_position[var1]['row'],
                                                                  'col': self.element_position[var1]['col'] + 1,
                                                                  'rowspan': self.element_position[var1]['rowspan']}})
                    Label(self.main_frame, image=self.img[self.count_img]).grid(
                        row=self.element_position[f'{ch}{var1}']['row'],
                        column=self.element_position[f'{ch}{var1}']['col'],
                        rowspan=self.element_position[f'{ch}{var1}']['rowspan'], sticky=NS)
                    self.rows[self.element_position[var1]['row']] += 1  # переходим на след столбец
                    self.count_img += 1

                elif len(self.stack) > 1:

                    var1 = self.stack.pop()
                    var2 = self.stack.pop()

                    # Обновляем информацию о переменных
                    self.stack.append(f'{var2} {ch} {var1}')

                    # Выравниваем до одного столбца
                    self.round_rows(var1, var2)

                    # После того, как сравняли до одного столбца, рисуем соединялки
                    if self.element_position[var1]['row'] < self.element_position[var2]['row']:
                        _top_row = self.element_position[var1]['row']
                        _bot_row = self.element_position[var2]['row']
                        _top_span = self.element_position[var1]['rowspan']
                        _bot_span = self.element_position[var2]['rowspan']

                    elif self.element_position[var1]['row'] > self.element_position[var2]['row']:
                        _top_row = self.element_position[var2]['row']
                        _bot_row = self.element_position[var1]['row']
                        _top_span = self.element_position[var2]['rowspan']
                        _bot_span = self.element_position[var1]['rowspan']

                    else:
                        _top_row = _bot_row = self.element_position[var1]['row']
                        _top_span = _bot_span = self.element_position[var1]['rowspan']

                    # Первое - спены = 1
                    if self.element_position[var1]['rowspan'] == 1 and self.element_position[var2]['rowspan'] == 1:

                        self.img.append(ImageTk.PhotoImage(self.all_img['b1']))
                        Label(self.main_frame, image=self.img[self.count_img]).grid(row=_top_row,
                                                                                    column=self.rows[_top_row],
                                                                                    rowspan=1, sticky=NS)
                        self.rows[_top_row] += 1  # переходим на след столбец
                        self.count_img += 1

                        self.img.append(ImageTk.PhotoImage(self.all_img['t1']))
                        Label(self.main_frame, image=self.img[self.count_img]).grid(row=_bot_row,
                                                                                    column=self.rows[_bot_row],
                                                                                    rowspan=1, sticky=NS)
                        self.rows[_bot_row] += 1  # переходим на след столбец
                        self.count_img += 1

                    # Если спены равны и = степени 2
                    else:
                        _lines_for_span = 0

                        self.img.append(ImageTk.PhotoImage(self.all_img['b1']))
                        Label(self.main_frame, image=self.img[self.count_img]).grid(row=_top_row,
                                                                                    column=self.rows[_top_row],
                                                                                    rowspan=_top_span, sticky=NS)
                        self.rows[_top_row] += 1  # переходим на след столбец
                        self.count_img += 1

                        self.img.append(ImageTk.PhotoImage(self.all_img['t1']))
                        Label(self.main_frame, image=self.img[self.count_img]).grid(row=_bot_row,
                                                                                    column=self.rows[_bot_row],
                                                                                    rowspan=_bot_span, sticky=NS)
                        self.rows[_bot_row] += 1  # переходим на след столбец
                        self.count_img += 1

                        _lines_for_span += 1
                        _rowspan_change = 1
                        _next_row = 0

                        while _lines_for_span < _top_span:
                            self.img.append(ImageTk.PhotoImage(self.all_img['b2']))
                            Label(self.main_frame, image=self.img[self.count_img]).grid(
                                row=_top_row + _top_span // 2 + _next_row,
                                column=self.rows[_top_row],
                                rowspan=_rowspan_change, sticky=NS)
                            self.rows[_top_row] += 1  # переходим на след столбец
                            self.count_img += 1

                            self.img.append(ImageTk.PhotoImage(self.all_img['t2']))
                            Label(self.main_frame, image=self.img[self.count_img]).grid(
                                row=_bot_row + _bot_span - (_bot_span // 2 + _rowspan_change + _next_row),
                                column=self.rows[_bot_row],
                                rowspan=_rowspan_change, sticky=NS)
                            self.rows[_bot_row] += 1  # переходим на след столбец
                            self.count_img += 1

                            _rowspan_change = 1 if _rowspan_change == 2 else 2
                            _lines_for_span += 1

                            # Если это четвертая соединялка или выше (главное, что четная)
                            if _lines_for_span >= 3 and (_lines_for_span & 1) == 1:
                                _next_row += 1

                    self.img.append(ImageTk.PhotoImage(self.all_img[ch]))
                    Label(self.main_frame, image=self.img[self.count_img]).grid(row=_top_row,
                                                                                column=self.rows[_top_row],
                                                                                rowspan=2 * _top_span, sticky=NS)

                    self.element_position.update({f'{var2} {ch} {var1}': {
                        'row': min(self.element_position[var2]['row'], self.element_position[var1]['row']),
                        'col': self.rows[_top_row],
                        'rowspan': 2 * _top_span}})

                    self.rows[_top_row] += 1  # переходим на след столбец
                    self.rows[_bot_row] += 1  # переходим на след столбец
                    self.count_img += 1

