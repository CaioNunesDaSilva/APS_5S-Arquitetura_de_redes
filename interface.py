from abc import ABC
from abc import abstractmethod
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from threading import Thread

from auxiliar import *
from constantes import *


class Interface(ABC):
    def __init__(self, tk):
        self._tk = tk
        self._iniciar_interface()

    def _iniciar_interface(self):
        self._tk.resizable(False, False)
        self._tk["background"] = COR_DE_FUNDO_PADRAO
        self._iniciar_tela()
        self._tk.protocol("WM_DELETE_WINDOW", self._fechar)
        self._tk.mainloop()

    @abstractmethod
    def _iniciar_tela(self):
        pass

    def _mudar_titulo(self, titulo: str):
        self._tk.title(titulo)

    @abstractmethod
    def _fechar(self):
        pass


class Login(Interface):
    def _iniciar_tela(self):
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

    def __limpar_campos(self):
        self.entry_name.delete(0, "end")
        self.entry_pswd.delete(0, "end")

    def __acao_btn_n_usr(self):
        self.main_frame.destroy()
        Cadastro(self._tk)

    def __acao_btn_logon(self):
        soquete = socket(AF_INET, SOCK_STREAM)
        soquete.connect((SOCKET_ENDERECO, SOCKET_PORTA))

        soquete.send(codificar(PedidoLogin(self.entry_name.get().strip(), self.entry_pswd.get().strip())))

        dados_cliente = descodificar(soquete.recv(BUFFER), Usuario)

        if dados_cliente:
            self.main_frame.destroy()
            MenuPrincipal(self._tk, dados_cliente, soquete)
        else:
            showerror(title="ERRO", message="Usuario nao cadastrado")
            self.__limpar_campos()

    def _fechar(self):
        self._tk.destroy()


class Cadastro(Interface):
    def _iniciar_tela(self):
        self._mudar_titulo("CADASTRO")
        self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.logo_img = PhotoImage(file=LOGO_CAMINHO)
        self.frame_logo = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=10, pady=5)
        self.label_logo = Label(self.frame_logo, image=self.logo_img, borderwidth=0)

        self.frame_logo.pack()
        self.label_logo.pack()

        self.frame_entry = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.label_name = Label(self.frame_entry, text="Nome", bg=COR_DE_FUNDO_PADRAO, font=FONTE_LABEL_CADASTRO)
        self.entry_name = Entry(self.frame_entry, borderwidth=2, width=18, font=FONTE_ENTRY_CADASTRO)
        self.label_pswd = Label(self.frame_entry, text="Senha", bg=COR_DE_FUNDO_PADRAO, font=FONTE_LABEL_CADASTRO)
        self.entry_pswd = Entry(self.frame_entry, borderwidth=2, width=18, show="*", font=FONTE_ENTRY_CADASTRO)

        self.frame_entry.grid_rowconfigure(1, minsize=50)
        self.frame_entry.grid_rowconfigure(3, minsize=50)
        self.frame_entry.grid_rowconfigure(5, minsize=50)

        self.frame_entry.pack(fill=X)
        self.label_name.grid(row=0, column=0, sticky=W)
        self.entry_name.grid(row=1, column=0, sticky=W+N)
        self.label_pswd.grid(row=2, column=0, sticky=W)
        self.entry_pswd.grid(row=3, column=0, sticky=W+N)

        self.frame_btn = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.btn_n_usr = Button(self.frame_btn, text="CADASTRAR", padx=5, pady=2, font=FONTE_BTN_CADASTRO,
                                command=self.__acao_btn_n_usr)
        self.btn_back = Button(self.frame_btn, text="VOLTAR", padx=5, pady=2, font=FONTE_BTN_CADASTRO,
                               command=self.__acao_btn_back)

        self.frame_btn.grid_columnconfigure(1, minsize=10)

        self.frame_btn.pack()
        self.btn_n_usr.grid(row=0, column=2, sticky=W)
        self.btn_back.grid(row=0, column=0, sticky=E)

    def __limpar_campos(self):
        self.entry_name.delete(0, "end")
        self.entry_pswd.delete(0, "end")

    def __acao_btn_back(self):
        self.main_frame.destroy()
        Login(self._tk)

    def __acao_btn_n_usr(self):
        soquete = socket(AF_INET, SOCK_STREAM)
        soquete.connect((SOCKET_ENDERECO, SOCKET_PORTA))

        soquete.send(codificar(PedidoCadastroUsuario(str(self.entry_name.get()).strip(),
                                                     str(self.entry_pswd.get()).strip())))

        if descodificar(soquete.recv(BUFFER), bool):
            showinfo(title="AVISO", message="Usuario cadastrado com sucesso")
        else:
            showerror(title="ERRO", message="Usuario ja cadastrado")

        soquete.close()

        self.__limpar_campos()

    def _fechar(self):
        self._tk.destroy()


class MenuPrincipal(Interface):
    def __init__(self, tk, dados_cliente: Usuario, soquete: socket):
        self.soquete = soquete
        self.dados_cliente = dados_cliente
        super().__init__(tk)

    def _iniciar_tela(self):
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

        self.btn_users = Button(self.frame_botoes, text="USUARIOS ONLINE", font=FONTE_BTN_MENU,
                                width=15, padx=10, pady=5, command=self.__acao_btn_users)
        self.btn_users.grid(row=0, column=0, pady=3)
        self.btn_groups = Button(self.frame_botoes, text="GRUPOS", font=FONTE_BTN_MENU,
                                 width=15, padx=10, pady=5, command=self.__acao_btn_groups)
        self.btn_groups.grid(row=1, column=0, pady=3)
        self.btn_exit = Button(self.frame_botoes, text="SAIR", font=FONTE_BTN_MENU,
                               width=15, padx=10, pady=5, command=self.__acao_btn_exit)
        self.btn_exit.grid(row=3, column=0, pady=3)

    def __acao_btn_users(self):
        self.main_frame.destroy()
        MenuUsuarios(self._tk, self.dados_cliente, self.soquete)

    def __acao_btn_groups(self):
        self.main_frame.destroy()
        MenuGrupos(self._tk, self.dados_cliente, self.soquete)

    def __acao_btn_exit(self):
        self.soquete.send(codificar(PedidoDesconectar(self.dados_cliente)))

        if descodificar(self.soquete.recv(BUFFER), bool):
            self.soquete.close()
            self.main_frame.destroy()
            Login(self._tk)

    def _fechar(self):
        self.soquete.send(codificar(PedidoDesconectar(self.dados_cliente)))

        if descodificar(self.soquete.recv(BUFFER), bool):
            self.soquete.close()
            self._tk.destroy()


class MenuUsuarios(Interface):
    def __init__(self, tk, dados_cliente: Usuario, soquete: socket):
        self.soquete = soquete
        self.dados_cliente = dados_cliente
        self.usuarios_online = self.__atualizar_usuarios_online()
        super().__init__(tk)

    def _iniciar_tela(self):
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

        self.__carregar_botoes_usuarios()

        self.frame_botoes = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.frame_botoes.pack(fill=BOTH, expand=True)

    def __atualizar_usuarios_online(self):
        self.soquete.send(codificar(PedidoAtualizarListaClientes(self.dados_cliente)))

        return descodificar(self.soquete.recv(BUFFER), [Usuario])

    def __carregar_botoes_usuarios(self):
        self.frame_botoes_usuarios = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)

        for usuario in self.usuarios_online:
            Button(self.frame_botoes_usuarios, text=usuario.nome, font=FONTE_BTN_USUARIOS,
                   background=COR_DE_FUNDO_BTN_LISTA,
                   command=lambda destinatario=usuario.nome: self.__acao_botoes_usuarios(destinatario)).pack()

        self.frame_botoes_usuarios.pack()

    def __acao_btn_refresh(self):
        self.usuarios_online = self.__atualizar_usuarios_online()

        self.frame_botoes_usuarios.destroy()

        self.__carregar_botoes_usuarios()

        self.label_info["text"] = f"{len(self.usuarios_online)} usuarios online"

    def __acao_botoes_usuarios(self, destinatario: str):
        self.main_frame.destroy()
        ChatUsuario(self._tk, self.dados_cliente, destinatario, self.soquete)

    def __acao_btn_exit(self):
        self.main_frame.destroy()
        MenuPrincipal(self._tk, self.dados_cliente, self.soquete)

    def _fechar(self):
        self.soquete.send(codificar(PedidoDesconectar(self.dados_cliente)))

        if descodificar(self.soquete.recv(BUFFER), bool):
            self.soquete.close()
            self._tk.destroy()


class MenuGrupos(Interface):
    def __init__(self, tk, dados_cliente: Usuario, soquete: socket):
        self.soquete = soquete
        self.dados_cliente = dados_cliente
        self.grupos_participante = self.__atualizar_grupos_participantes()
        super().__init__(tk)

    def _iniciar_tela(self):
        self._mudar_titulo("GRUPOS")
        self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.frame_header = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)

        self.label_info = Label(self.frame_header, text=f"{len(self.grupos_participante)} grupos",
                                font=FONTE_INFO_GRUPOS, background=COR_DE_FUNDO_PADRAO, borderwidth=0)
        self.label_info.grid(row=0, column=0, padx=3, pady=3)

        self.btn_refresh = Button(self.frame_header, text="Atualizar", font=FONTE_BTN_GRUPOS,
                                  width=15, padx=10, pady=5, command=self.__acao_btn_refresh)
        self.btn_refresh.grid(row=0, column=1, padx=3, pady=3)

        self.btn_nw_group = Button(self.frame_header, text="Novo Grupo", font=FONTE_BTN_GRUPOS,
                                   width=15, padx=10, pady=5, command=self.__acao_btn_nw_group)
        self.btn_nw_group.grid(row=0, column=2, padx=3, pady=3)

        self.btn_exit = Button(self.frame_header, text="Sair", font=FONTE_BTN_GRUPOS,
                               width=15, padx=3, pady=3, command=self.__acao_btn_exit)
        self.btn_exit.grid(row=0, column=3, padx=3, pady=3)

        self.frame_header.pack()

        self.__carregar_botoes_grupo()

        self.frame_botoes = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.frame_botoes.pack(fill=BOTH, expand=True)

    def __atualizar_grupos_participantes(self):
        self.soquete.send(codificar(PedidoAtualizarListaGrupos(self.dados_cliente)))

        return descodificar(self.soquete.recv(BUFFER), [Grupo])

    def __carregar_botoes_grupo(self):
        self.frame_botoes_grupos = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)

        for grupo in self.grupos_participante:
            Button(self.frame_botoes_grupos, text=grupo.nome, font=FONTE_BTN_GRUPOS,
                   background=COR_DE_FUNDO_BTN_LISTA,
                   command=lambda groupname=grupo.nome: self.__acao_botoes_grupos(groupname)).pack()

        self.frame_botoes_grupos.pack()

    def __acao_botoes_grupos(self, grupo: str):
        self.main_frame.destroy()
        ChatGrupo(self._tk, self.dados_cliente, grupo, self.soquete)

    def __acao_btn_refresh(self):
        self.grupos_participante = self.__atualizar_grupos_participantes()

        self.frame_botoes_grupos.destroy()

        self.__carregar_botoes_grupo()

        self.label_info["text"] = f"{len(self.grupos_participante)} grupos"

    def __acao_btn_nw_group(self):
        self.main_frame.destroy()
        CadastroGrupo(self._tk, self.dados_cliente, self.soquete)

    def __acao_btn_exit(self):
        self.main_frame.destroy()
        MenuPrincipal(self._tk, self.dados_cliente, self.soquete)

    def _fechar(self):
        self.soquete.send(codificar(PedidoDesconectar(self.dados_cliente)))

        if descodificar(self.soquete.recv(BUFFER), bool):
            self.soquete.close()
            self._tk.destroy()


class ChatUsuario(Interface):
    def __init__(self, tk, dados_cliente: Usuario, destinatario: str, soquete: socket):
        self.soquete = soquete
        self.dados_cliente = dados_cliente
        self.destinatario = destinatario
        super().__init__(tk)

    def _iniciar_tela(self):
        self._mudar_titulo(f"Chat - {self.destinatario}")

        self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.main_frame.grid_rowconfigure(1, minsize=10)
        self.main_frame.grid_columnconfigure(1, minsize=15)
        self.main_frame.grid_columnconfigure(3, minsize=10)
        self.main_frame.pack(fill=X)

        self.recv_area = ScrolledText(self.main_frame, font=FONTE_CHAT_MENSAGEM_RECEBIDA,
                                      borderwidth=2, width=80, height=20)
        self.recv_area.configure(state=DISABLED, wrap=WORD)
        self.recv_area.grid(row=0, column=0)

        self.send_area = ScrolledText(self.main_frame, font=FONTE_CHAT_MENSAGEM_ENVIADA,
                                      borderwidth=2, width=80, height=5)
        self.send_area.configure(wrap=WORD)
        self.send_area.grid(row=2, column=0)

        self.btn_exit = Button(self.main_frame, text="SAIR", font=FONTE_CHAT_BTN_SAIR, padx=50, pady=20,
                               command=self.__acao_btn_exit)
        self.btn_exit.grid(row=1, column=2)

        self.btn_send = Button(self.main_frame, text="ENVIAR", font=FONTE_CHAT_BTN_ENVIAR, padx=50, pady=20,
                               command=self.__enviar_mensagem)
        self.btn_send.grid(row=2, column=2)

        self.soquete.send(codificar(PedidoMensagensPrivadasArquivadas(self.dados_cliente, self.destinatario)))

        mensagens_arquivadas = descodificar(self.soquete.recv(BUFFER), [MensagemPrivada])

        if mensagens_arquivadas:
            for mensagem in mensagens_arquivadas:
                if mensagem:
                    self.__mostrar_mensagem(mensagem)

        self.receber_mensagens = Thread(target=self.__receber_mensagens)
        self.receber_mensagens.start()

    def __mostrar_mensagem(self, msg: MensagemPrivada):
        self.recv_area.configure(state=NORMAL)

        self.recv_area.insert(END, f"{msg.remetente.nome}: {msg.mensagem}")
        self.recv_area.insert(END, "\n")

        self.recv_area.configure(state=DISABLED)
        self.recv_area.see(END)

    def __enviar_mensagem(self):
        msg = self.send_area.get("1.0", END).strip()
        self.send_area.delete("1.0", END)
        msg = MensagemPrivada(self.dados_cliente, msg, self.destinatario)
        self.__mostrar_mensagem(msg)
        self.soquete.send(codificar(msg))

    def __receber_mensagens(self):
        while True:
            msg = descodificar(self.soquete.recv(BUFFER), Pedido)
            if msg:
                self.__mostrar_mensagem(msg)
            else:
                break

    def __acao_btn_exit(self):
        self.soquete.send(codificar(None))
        self.receber_mensagens.join()

        self.main_frame.destroy()
        MenuUsuarios(self._tk, self.dados_cliente, self.soquete)

    def _fechar(self):
        self.soquete.send(codificar(None))
        self.receber_mensagens.join()
        self.soquete.send(codificar(PedidoDesconectar(self.dados_cliente)))

        if descodificar(self.soquete.recv(BUFFER), bool):
            self.soquete.close()
            self._tk.destroy()


class ChatGrupo(Interface):
    def __init__(self, tk, dados_cliente: Usuario, grupo: str, soquete: socket):
        self.soquete = soquete
        self.dados_cliente = dados_cliente
        self.grupo = grupo
        super().__init__(tk)

    def _iniciar_tela(self):
        self._mudar_titulo(f"Chat - {self.grupo}")

        self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.main_frame.grid_rowconfigure(1, minsize=10)
        self.main_frame.grid_columnconfigure(1, minsize=15)
        self.main_frame.grid_columnconfigure(3, minsize=10)
        self.main_frame.pack(fill=X)

        self.recv_area = ScrolledText(self.main_frame, font=FONTE_CHAT_MENSAGEM_RECEBIDA,
                                      borderwidth=2, width=80, height=20)
        self.recv_area.configure(state=DISABLED, wrap=WORD)
        self.recv_area.grid(row=0, column=0)

        self.send_area = ScrolledText(self.main_frame, font=FONTE_CHAT_MENSAGEM_ENVIADA,
                                      borderwidth=2, width=80, height=5)
        self.send_area.configure(wrap=WORD)
        self.send_area.grid(row=2, column=0)

        self.btn_exit = Button(self.main_frame, text="SAIR", font=FONTE_CHAT_BTN_SAIR, padx=50, pady=20,
                               command=self.__acao_btn_exit)
        self.btn_exit.grid(row=1, column=2)

        self.btn_send = Button(self.main_frame, text="ENVIAR", font=FONTE_CHAT_BTN_ENVIAR, padx=50, pady=20,
                               command=self.__enviar_mensagem)
        self.btn_send.grid(row=2, column=2)

        self.soquete.send(codificar(PedidoMensagensGrupoArquivadas(self.dados_cliente, self.grupo)))

        mensagens_arquivadas = descodificar(self.soquete.recv(BUFFER), [MensagemGrupo])

        if mensagens_arquivadas:
            for mensagem in mensagens_arquivadas:
                if mensagem:
                    self.__mostrar_mensagem(mensagem)

        self.receber_mensagens = Thread(target=self.__receber_mensagens)
        self.receber_mensagens.start()

    def __mostrar_mensagem(self, msg: MensagemGrupo):
        self.recv_area.configure(state=NORMAL)

        self.recv_area.insert(END, f"{msg.remetente.nome}: {msg.mensagem}")
        self.recv_area.insert(END, "\n")

        self.recv_area.configure(state=DISABLED)
        self.recv_area.see(END)

    def __enviar_mensagem(self):
        msg = self.send_area.get("1.0", END).strip()
        self.send_area.delete("1.0", END)
        msg = MensagemGrupo(self.dados_cliente, msg, self.grupo)
        self.__mostrar_mensagem(msg)
        self.soquete.send(codificar(msg))

    def __receber_mensagens(self):
        while True:
            msg = descodificar(self.soquete.recv(BUFFER), Pedido)
            if msg:
                self.__mostrar_mensagem(msg)
            else:
                break

    def __acao_btn_exit(self):
        self.soquete.send(codificar(None))
        self.receber_mensagens.join()

        self.main_frame.destroy()
        MenuGrupos(self._tk, self.dados_cliente, self.soquete)

    def _fechar(self):
        self.soquete.send(codificar(None))
        self.receber_mensagens.join()
        self.soquete.send(codificar(PedidoDesconectar(self.dados_cliente)))

        if descodificar(self.soquete.recv(BUFFER), bool):
            self.soquete.close()
            self._tk.destroy()


class CadastroGrupo(Interface):
    def __init__(self, tk, dados_cliente: Usuario, soquete: socket):
        self.soquete = soquete
        self.dados_cliente = dados_cliente
        super().__init__(tk)

    def _iniciar_tela(self):
        self._mudar_titulo("Cadastrar Grupo")
        self.main_frame = Frame(self._tk, bg=COR_DE_FUNDO_PADRAO)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.frame_entry = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.label_name = Label(self.frame_entry, text="Nome do Grupo", bg=COR_DE_FUNDO_PADRAO,
                                font=FONTE_LABEL_CADASTRO)
        self.entry_name = Entry(self.frame_entry, borderwidth=2, width=18, font=FONTE_ENTRY_CADASTRO)

        self.label_members = Label(self.frame_entry, text="Integrantes", bg=COR_DE_FUNDO_PADRAO,
                                   font=FONTE_LABEL_CADASTRO)
        self.entry_members = Entry(self.frame_entry, borderwidth=2, width=18, font=FONTE_ENTRY_CADASTRO)

        self.frame_entry.grid_rowconfigure(1, minsize=50)
        self.frame_entry.grid_rowconfigure(3, minsize=50)
        self.frame_entry.grid_rowconfigure(5, minsize=50)

        self.frame_entry.pack(fill=X)
        self.label_name.grid(row=0, column=0, sticky=W)
        self.entry_name.grid(row=1, column=0, sticky=W+N)
        self.label_members.grid(row=2, column=0, sticky=W)
        self.entry_members.grid(row=3, column=0, sticky=W+N)

        self.label_info = Label(self.main_frame,
                                text="digite o nome dos integrantes, sem espaco, separados por virgula",
                                bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.label_info.pack()

        self.frame_btn = Frame(self.main_frame, bg=COR_DE_FUNDO_PADRAO, padx=5, pady=5)
        self.btn_nw_group = Button(self.frame_btn, text="CADASTRAR", padx=5, pady=2, font=FONTE_BTN_CADASTRO,
                                   command=self.__acao_btn_nw_group)
        self.btn_back = Button(self.frame_btn, text="VOLTAR", padx=5, pady=2, font=FONTE_BTN_CADASTRO,
                               command=self.__acao_btn_back)

        self.frame_btn.grid_columnconfigure(1, minsize=10)

        self.frame_btn.pack()
        self.btn_nw_group.grid(row=0, column=2, sticky=W)
        self.btn_back.grid(row=0, column=0, sticky=E)

    def __limpar_campos(self):
        self.entry_name.delete(0, "end")
        self.entry_members.delete(0, "end")

    def __acao_btn_nw_group(self):
        self.soquete.send(codificar(PedidoCadastroGrupo(self.dados_cliente,
                                                        str(self.entry_name.get()).strip(),
                                                        str(self.entry_members.get()).strip().split(","))))

        resultado = descodificar(self.soquete.recv(BUFFER), bool)

        if resultado:
            showinfo(title="AVISO", message="Grupo cadastrado com sucesso")
        else:
            showerror(title="ERRO", message="Grupo ja cadastrado")

        self.__limpar_campos()

    def __acao_btn_back(self):
        self.main_frame.destroy()
        MenuGrupos(self._tk, self.dados_cliente, self.soquete)

    def _fechar(self):
        self.soquete.send(codificar(PedidoDesconectar(self.dados_cliente)))

        if descodificar(self.soquete.recv(BUFFER), bool):
            self.soquete.close()
            self._tk.destroy()
