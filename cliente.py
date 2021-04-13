from tkinter import Tk

from interface import Login


if __name__ == "__main__":
    try:
        tela = Tk()
        Login(tela)

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: cliente\nMain")
        print(erro)
