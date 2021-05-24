from tkinter import Tk
from tkinter.messagebox import showerror

from interface import Login

if __name__ == "__main__":
    try:
        tela = Tk()
        Login(tela)

    except Exception as erro:
        showerror(title="ERRO", message=f"ocorreu o erro {erro}, reinicie o programa")


