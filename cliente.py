from tkinter import Tk
from tkinter.messagebox import showerror

if __name__ == "__main__":
    try:
        tela = Tk()
    # TODO too broad exception clause
    except Exception as erro:
        print(erro)
        showerror(title="ERRO", message="Ocorreu um erro inesperado que impossibilitou a execução do programa.")
