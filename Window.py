from TruthTable import *
from Scheme import *


class Window:
    def __init__(self, width, height, resizable=(False, False), title='Cody', icon=None):
        self.width = width
        self.height = height

        self.root = Tk()  # Инициализация окна
        self.centering_window()
        self.root.resizable(resizable[0], resizable[1])
        self.root.title(title)
        if icon is not None:
            self.root.iconbitmap(icon)

        self.TRUE_FALSE = BooleanVar(value=False)  # Флаги для программы
        self.SIMPLE = BooleanVar(value=True)
        self.source_string = ''  # Переменные для отрисовки
        self.entry = Entry(self.root, width=20, bg='#e0bede', font='SegoeUI 20', fg='#3b4559', justify=CENTER)

        # Дочернее окно
        self.child_window = ''

    def centering_window(self):
        x = (self.root.winfo_screenwidth() - self.width) / 2
        y = (self.root.winfo_screenheight() - self.height) / 2
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

    def run(self):
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
        Label(self.root, width=20, height=2, bg='#e5d3e4', text='Введите выражение',
              font='SegoeUI 20', fg='#212d30').grid(columnspan=4, sticky=W + E)

        self.entry.grid(columnspan=4, sticky=W + E)

        _t = ('1/0', 'True/False', 'Simple', 'Hard')
        _v = (False, True, True, False)
        _a = (self.action_1_0, self.action_true_false, self.action_simple, self.action_hard)

        for i in range(2):
            Radiobutton(self.root, text=_t[i], variable=self.TRUE_FALSE, value=_v[i], width=18, height=3, bg='#e5d3e4',
                        fg='#212d30', activebackground='#efece6', activeforeground='#212d30',
                        font=('SegoeUI', 12, 'bold'),
                        command=_a[i]).grid(row=2 + i, columnspan=2, sticky=W + E)
            Radiobutton(self.root, text=_t[2 + i], variable=self.SIMPLE, value=_v[2 + i], width=18, height=3, bg='#e5d3e4',
                        fg='#212d30', activebackground='#efece6', activeforeground='#212d30',
                        font=('SegoeUI', 12, 'bold'),
                        command=_a[2 + i]).grid(row=2 + i, column=2, columnspan=2, sticky=W + E)

        Button(self.root, width=20, height=1, text='Выполнить', font='SegoeUI 20', bg='#e5d3e4',
               fg='red', activeforeground='red', activebackground='#efece6', command=self.create_data
               ).grid(columnspan=4, sticky=W + E)

    def action_true_false(self):
        self.TRUE_FALSE = BooleanVar(value=True)

    def action_1_0(self):
        self.TRUE_FALSE = BooleanVar(value=False)

    def action_simple(self):
        self.SIMPLE = BooleanVar(value=True)

    def action_hard(self):
        self.SIMPLE = BooleanVar(value=False)

    def create_data(self):
        self.source_string = self.entry.get().replace(' ', '').split('#')
        print(self.source_string, '-', len(self.source_string))

        if len(self.source_string) > 1:
            p = create_priorities(self.source_string[1])  # Создаем таблицу
            r = remake_to_rev_pol_not(self.source_string[0], p)
            t = create_truth_table(r, list(self.source_string[1].replace(',', '')))
            create_excel_file(t, self.TRUE_FALSE.get())

            # Рисуем схему
            self.child_window = Scheme(self.root, self.width * 3, int(self.height * 2.3), (False, False), 'Scheme',
                                       simple=self.SIMPLE.get())
            self.child_window.draw(r, list(self.source_string[1].replace(',', '')))
