from tkinter import Tk
from tkinter.messagebox import showerror

from interface import Login


if __name__ == "__main__":
    try:
        tela = Tk()
        Login(tela)

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: cliente")
        print(erro)
        showerror(title="ERRO", message="Ocorreu um erro inesperado que impossibilitou a execução do programa.")
