try:
    from tkinter import Tk
    from tkinter.messagebox import showerror

    from interface import Login

except ImportError:
    print("Erro na importacao de modululos necessarios para inicar o programa")
    input()
    exit()

if __name__ == "__main__":
    tela = Tk()
    Login(tela)
