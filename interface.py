from abc import ABC
from abc import abstractmethod
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM

from auxiliar import *
from constantes import *


class Interface(ABC):
    def __init__(self, tk):
        try:
            self._tk = tk
            self._iniciar_interface()

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Interface\nMetodo: __init__")
            print(erro)

    def _iniciar_interface(self):
        try:
            self._tk.resizable(False, False)
            self._tk["background"] = COR_DE_FUNDO_PADRAO
            self._iniciar_tela()
            self._tk.mainloop()

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Interface\nMetodo: _iniciar_interface")
            print(erro)

    @abstractmethod
    def _iniciar_tela(self):
        pass

    def _mudar_titulo(self, titulo):
        try:
            self._tk.title(titulo)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Interface\nMetodo: _mudar_titulo")
            print(erro)

    def _fechar(self):
        try:
            self._tk.destroy()

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Interface\nMetodo: _fechar")
            print(erro)


class Login(Interface):
    def _iniciar_tela(self):
        try:
            self._mudar_titulo("LOGIN")
            self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
            self.main_frame.pack(fill=BOTH, expand=True)

            self.logo_img = PhotoImage(file=LOGO_CAMINHO)
            self.frame_logo = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=10, pady=5)
            self.label_logo = Label(self.frame_logo, image=self.logo_img, borderwidth=0)

            self.frame_logo.pack()
            self.label_logo.pack()

            self.frame_entry = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
            self.label_name = Label(self.frame_entry, text="Nome", bg=COR_DE_FUNDO_PADRAO, font=FONTE_LABEL_LOGIN)
            self.entry_name = Entry(self.frame_entry, borderwidth=2, width=18, font=FONTE_ENTRY_LOGIN)
            self.label_pswd = Label(self.frame_entry, text="Senha", bg=COR_DE_FUNDO_PADRAO, font=FONTE_LABEL_LOGIN)
            self.entry_pswd = Entry(self.frame_entry, borderwidth=2, width=18, show="*", font=FONTE_ENTRY_LOGIN)

            self.frame_entry.grid_rowconfigure(1, minsize=60)
            self.frame_entry.grid_rowconfigure(3, minsize=60)

            self.entry_name.focus_force()

            self.frame_entry.pack(fill=X)
            self.label_name.grid(row=0, column=0, sticky=W)
            self.entry_name.grid(row=1, column=0, sticky=W + N)
            self.label_pswd.grid(row=2, column=0, sticky=W)
            self.entry_pswd.grid(row=3, column=0, sticky=W + N)

            self.frame_btn = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
            self.btn_logon = Button(self.frame_btn, text="ENTRAR", padx=5, pady=2, font=FONTE_BTN_LOGIN,
                                    command=self.__acao_btn_logon)
            self.btn_n_usr = Button(self.frame_btn, text="NOVO", padx=5, pady=2, font=FONTE_BTN_LOGIN,
                                    command=self.__acao_btn_n_usr)

            self.frame_btn.grid_columnconfigure(1, minsize=40)

            self.frame_btn.pack()
            self.btn_logon.grid(row=0, column=0, sticky=E)
            self.btn_n_usr.grid(row=0, column=2, sticky=W)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Login\nMetodo: _iniciar_tela")
            print(erro)

    def __acao_btn_n_usr(self):
        try:
            self.main_frame.destroy()
            Cadastro(self._tk)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Login\nMetodo: __acao_btn_n_usr")
            print(erro)

    def __acao_btn_logon(self):
        try:
            soquete = socket(AF_INET, SOCK_STREAM)
            soquete.connect((SOCKET_ENDERECO, SOCKET_PORTA))

            pedido_login = {"tipo": 1, "nome": self.entry_name.get().strip(),
                            "senha": self.entry_pswd.get().strip()}
            soquete.send(codificar(pedido_login))

            dados_cliente = descodificar(soquete.recv(BUFFER))
            dados_cliente = Usuario.usuario_from_dict(dados_cliente)

            if dados_cliente:
                self.main_frame.destroy()
                MenuPrincipal(self._tk, dados_cliente, soquete)
            else:
                showerror(title="ERRO", message="Usuario nao cadastrado")

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Login\nMetodo: __acao_btn_logon")
            print(erro)


class Cadastro(Interface):
    def _iniciar_tela(self):
        try:
            self._mudar_titulo("CADASTRO")
            self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
            self.main_frame.pack(fill=BOTH, expand=True)

            self.logo_img = PhotoImage(file=LOGO_CAMINHO)
            self.frame_logo = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=10, pady=5)
            self.label_logo = Label(self.frame_logo, image=self.logo_img, borderwidth=0)

            self.frame_logo.pack()
            self.label_logo.pack()

            self.frame_entry = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
            self.label_name = Label(self.frame_entry, text="Nome", bg=COR_DE_FUNDO_PADRAO, font=FONTE_LABEL_LOGIN)
            self.entry_name = Entry(self.frame_entry, borderwidth=2, width=18, font=FONTE_ENTRY_LOGIN)
            self.label_pswd = Label(self.frame_entry, text="Senha", bg=COR_DE_FUNDO_PADRAO, font=FONTE_LABEL_LOGIN)
            self.entry_pswd = Entry(self.frame_entry, borderwidth=2, width=18, show="*", font=FONTE_ENTRY_LOGIN)

            self.frame_entry.grid_rowconfigure(1, minsize=50)
            self.frame_entry.grid_rowconfigure(3, minsize=50)
            self.frame_entry.grid_rowconfigure(5, minsize=50)

            self.frame_entry.pack(fill=X)
            self.label_name.grid(row=0, column=0, sticky=W)
            self.entry_name.grid(row=1, column=0, sticky=W+N)
            self.label_pswd.grid(row=2, column=0, sticky=W)
            self.entry_pswd.grid(row=3, column=0, sticky=W+N)

            self.frame_btn = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
            self.btn_n_usr = Button(self.frame_btn, text="CADASTRAR", padx=5, pady=2, font=FONTE_BTN_LOGIN,
                                    command=self.__acao_btn_n_usr)
            self.btn_back = Button(self.frame_btn, text="VOLTAR", padx=5, pady=2, font=FONTE_BTN_LOGIN,
                                   command=self.__acao_btn_back)

            self.frame_btn.grid_columnconfigure(1, minsize=10)

            self.frame_btn.pack()
            self.btn_n_usr.grid(row=0, column=2, sticky=W)
            self.btn_back.grid(row=0, column=0, sticky=E)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Cadastro\nMetodo: _iniciar_tela")
            print(erro)

    def __acao_btn_back(self):
        try:
            self.main_frame.destroy()
            Login(self._tk)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Cadastro\nMetodo: __acao_btn_back")
            print(erro)

    def __acao_btn_n_usr(self):
        try:
            soquete = socket(AF_INET, SOCK_STREAM)
            soquete.connect((SOCKET_ENDERECO, SOCKET_PORTA))

            pedido_cadastro = {"tipo": 0, "nome": str(self.entry_name.get()).strip(),
                               "senha": str(self.entry_pswd.get()).strip()}
            soquete.send(codificar(pedido_cadastro))

            resultado = descodificar(soquete.recv(BUFFER))

            if resultado:
                showinfo(title="AVISO", message="Usuario cadastrado com sucesso")
            else:
                showerror(title="ERRO", message="Usuario ja cadastrado")

            soquete.close()

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: Cadastro\nMetodo: __acao_btn_n_usr")
            print(erro)


class MenuPrincipal(Interface):
    def __init__(self, tk, dados_cliente: Usuario, soquete: socket):
        try:
            self.soquete = soquete
            self.dados_cliente = dados_cliente
            super().__init__(tk)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuPrincipal\nMetodo: __init__")
            print(erro)

    def _iniciar_tela(self):
        try:
            self._mudar_titulo("MENU")
            self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
            self.main_frame.pack(fill=BOTH, expand=True)

            self.logo_img = PhotoImage(file=LOGO_CAMINHO)
            self.frame_logo = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=10, pady=5)
            self.label_logo = Label(self.frame_logo, image=self.logo_img, borderwidth=0)

            self.frame_logo.pack()
            self.label_logo.pack()

            self.frame_botoes = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
            self.frame_botoes.pack(fill=BOTH, expand=True)

            self.btn_users = Button(self.frame_botoes, text="USUARIOS ONLINE", font=FONTE_BTN_MENU, width=15, padx=10, pady=5,
                                    command=self.__acao_btn_users)
            self.btn_users.grid(row=0, column=0, pady=3)
            self.btn_groups = Button(self.frame_botoes, text="GRUPOS", font=FONTE_BTN_MENU, width=15, padx=10, pady=5,
                                     command=self.__acao_btn_groups)
            self.btn_groups.grid(row=1, column=0, pady=3)
            self.btn_exit = Button(self.frame_botoes, text="SAIR", font=FONTE_BTN_MENU, width=15, padx=10, pady=5,
                                   command=self.__acao_btn_exit)
            self.btn_exit.grid(row=3, column=0, pady=3)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuPrincipal\nMetodo: _iniciar_tela")
            print(erro)

    def __acao_btn_users(self):
        try:
            self.main_frame.destroy()
            MenuUsuarios(self._tk, self.dados_cliente, self.soquete)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuPrincipal\nMetodo: __acao_btn_users")
            print(erro)

    def __acao_btn_groups(self):
        pass

    def __acao_btn_exit(self):
        try:
            if self.soquete:
                self.soquete.close()
            self.main_frame.destroy()
            Login(self._tk)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuPrincipal\nMetodo: __acao_btn_exit")
            print(erro)


class MenuUsuarios(Interface):
    def __init__(self, tk, dados_cliente: Usuario, soquete: socket):
        try:
            self.soquete = soquete
            self.dados_cliente = dados_cliente
            self.usuarios_online = self.__atualizar_usuarios_online()
            super().__init__(tk)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuUsuarios\nMetodo: __init__")
            print(erro)

    def _iniciar_tela(self):
        try:
            self._mudar_titulo("USUARIOS")
            self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
            self.main_frame.pack(fill=BOTH, expand=True)

            self.frame_header = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)

            self.label_info = Label(self.frame_header, text=f"{len(self.usuarios_online)} usuarios online",
                                    font=FONTE_INFO_USUARIOS, background=COR_DE_FUNDO_PADRAO, borderwidth=0)
            self.label_info.grid(row=0, column=0, padx=3, pady=3)

            self.btn_refresh = Button(self.frame_header, text="Atualizar", font=FONTE_BTN_USUARIOS,
                                      width=15, padx=10, pady=5, command=self.__acao_btn_refresh)
            self.btn_refresh.grid(row=0, column=1, padx=3, pady=3)

            self.btn_exit = Button(self.frame_header, text="Sair", font=FONTE_BTN_USUARIOS,
                                   width=15, padx=3, pady=3, command=self.__acao_btn_exit)
            self.btn_exit.grid(row=0, column=2, padx=3, pady=3)

            self.frame_header.pack()

            self.frame_botoes_usuarios = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)

            for usuario in self.usuarios_online:
                Button(self.frame_botoes_usuarios, text=usuario.nome, font=FONTE_BTN_USUARIOS,
                       background=COR_DE_FUNDO_BTN_USUARIOS).pack()

            self.frame_botoes_usuarios.pack()

            self.frame_botoes = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
            self.frame_botoes.pack(fill=BOTH, expand=True)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuUsuarios\nMetodo: _iniciar_tela")
            print(erro)

    def __atualizar_usuarios_online(self):
        try:
            pedido = {"tipo": TipoMenssagem.ATUALIZAR_LISTA_CLIENTES.value,
                      "cliente": self.dados_cliente}
            self.soquete.send(codificar(pedido))

            lista_usuarios = descodificar(self.soquete.recv(BUFFER))

            contagem = 0
            for usuario in lista_usuarios:
                usuario = descodificar(usuario)
                lista_usuarios[contagem] = Usuario.usuario_from_dict(usuario)

            return lista_usuarios

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuUsuarios\nMetodo: __atualizar_usuarios_online")
            print(erro)

    def __acao_btn_refresh(self):
        try:
            self.usuarios_online = self.__atualizar_usuarios_online()

            self.frame_botoes_usuarios.destroy()

            self.frame_botoes_usuarios = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)

            for usuario in self.usuarios_online:
                Button(self.frame_botoes_usuarios, text=usuario.nome, font=FONTE_BTN_USUARIOS,
                       background=COR_DE_FUNDO_BTN_USUARIOS).pack()

            self.frame_botoes_usuarios.pack()

            self.label_info["text"] = f"{len(self.usuarios_online)} usuarios online"

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuUsuarios\nMetodo: __acao_btn_refresh")
            print(erro)

    def __acao_btn_exit(self):
        try:
            self.main_frame.destroy()
            MenuPrincipal(self._tk, self.dados_cliente, self.soquete)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: interface\nClasse: MenuUsuarios\nMetodo: __acao_btn_exit")
            print(erro)
