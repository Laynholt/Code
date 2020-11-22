from tkinter import *

# Размер приложения
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


def main():
    window = Tk()
    window.title('GO to sleep!')
    window.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
    window.resizable(False, False)

    window.mainloop()


if __name__ == '__main__':
    main()

