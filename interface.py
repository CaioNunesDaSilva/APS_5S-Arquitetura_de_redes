from abc import ABC
from abc import abstractmethod
from tkinter import *

from constantes import COR_DE_FUNDO_PADRAO
from constantes import LOGO_TELA_DE_LOGIN
from constantes import LOGIN_FONTE_LABEL
from constantes import LOGIN_FONTE_ENTRY
from constantes import LOGIN_FONTE_BTN


class Interface(ABC):
    def __init__(self, tk, ):
        self._tk = tk
        self.__iniciar_interface()

    def __iniciar_interface(self):
        self._tk.resizable(False, False)
        self._tk["background"] = COR_DE_FUNDO_PADRAO
        self._init_tela()
        self._tk.mainloop()

    @abstractmethod
    def _init_tela(self):
        pass

    @abstractmethod
    def _mudar_janela(self, nova_janela):
        pass

    def _mudar_titulo(self, titulo):
        self._tk.title(titulo)

    def _fechar(self):
        self._tk.destroy()


class Login(Interface):
    def _init_tela(self):
        self._mudar_titulo("LOGIN")
        self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.logo_img = PhotoImage(file=LOGO_TELA_DE_LOGIN)
        self.frame_logo = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=10, pady=5)
        self.label_logo = Label(self.frame_logo, image=self.logo_img, borderwidth=0)

        self.frame_logo.pack()
        self.label_logo.pack()

        self.frame_entry = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.label_name = Label(self.frame_entry, text="Nome", bg=COR_DE_FUNDO_PADRAO, font=LOGIN_FONTE_LABEL)
        self.entry_name = Entry(self.frame_entry, borderwidth=2, width=18, font=LOGIN_FONTE_ENTRY)
        self.label_pswd = Label(self.frame_entry, text="Senha", bg=COR_DE_FUNDO_PADRAO, font=LOGIN_FONTE_LABEL)
        self.entry_pswd = Entry(self.frame_entry, borderwidth=2, width=18, show="*", font=LOGIN_FONTE_ENTRY)

        self.frame_entry.grid_rowconfigure(1, minsize=60)
        self.frame_entry.grid_rowconfigure(3, minsize=60)

        self.entry_name.focus_force()

        self.frame_entry.pack(fill=X)
        self.label_name.grid(row=0, column=0, sticky=W)
        self.entry_name.grid(row=1, column=0, sticky=W + N)
        self.label_pswd.grid(row=2, column=0, sticky=W)
        self.entry_pswd.grid(row=3, column=0, sticky=W + N)

        # TODO Botoes de acao
        self.frame_btn = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.btn_logon = Button(self.frame_btn, text="ENTRAR", padx=5, pady=2, font=LOGIN_FONTE_BTN,)#command=self.user_logon
        self.btn_n_usr = Button(self.frame_btn, text="NOVO", padx=5, pady=2, font=LOGIN_FONTE_BTN,)#command=self._change_window

        self.frame_btn.grid_columnconfigure(1, minsize=40)

        self.frame_btn.pack()
        self.btn_logon.grid(row=0, column=0, sticky=E)
        self.btn_n_usr.grid(row=0, column=2, sticky=W)

    def _mudar_janela(self, nova_janela):
        self.main_frame.destroy()
        nova_janela(self._tk)