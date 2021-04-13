from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from threading import Thread
from json import loads
from json import dumps

from auxiliar import *
from constantes import SOCKET_ENDERECO
from constantes import SOCKET_PORTA
from constantes import BUFFER
from db import debug_cadastrar
from db import debug_login
from db import debug_carregar_grupos


def aceitar_conexao():
    try:
        while THREAD_ACEITAR_CONEXAO:
            conexao, endereco = soquete.accept()
            print(f"NOVA CONEXAO: {conexao}, {endereco}")
            Thread(target=controlador_cliente, args=(conexao, endereco)).start()

    # TODO too broad exception clause
    except Exception as erro_thread:
        print("Modulo: servidor\nFuncao: aceitar_conexao")
        print(erro_thread)


def controlador_cliente(conexao, endereco):
    try:
        while True:
            dados_recebidos = conexao.recv(BUFFER)

            if dados_recebidos:
                dados_recebidos = dados_recebidos.decode()
                dados_recebidos = loads(dados_recebidos)

                pedido = TipoMenssagem.converter_valor_tipo(dados_recebidos["tipo"])

                if pedido == TipoMenssagem.CADASTRO_USUARIO:
                    dados_cadastro = dumps(debug_cadastrar(dados_recebidos["nome"], dados_recebidos["senha"]))
                    conexao.send(dados_cadastro.encode())
                    conexao.close()
                    break

                elif pedido == TipoMenssagem.LOGIN:
                    cliente = debug_login(dados_recebidos["nome"], dados_recebidos["senha"])

                    if cliente:
                        CLIENTES.append(cliente)

                    dados_enviar = dumps(cliente.to_json())
                    conexao.send(dados_enviar.encode())

    # TODO too broad exception clause
    except Exception as erro_thread:
        print("Modulo: servidor\nFuncao: controlador_cliente")
        print(erro_thread)


if __name__ == "__main__":
    try:
        CLIENTES = []
        GRUPOS = debug_carregar_grupos()

        soquete = socket(AF_INET, SOCK_STREAM)
        soquete.bind((SOCKET_ENDERECO, SOCKET_PORTA))
        soquete.listen()
        print("SERVIDOR AGUARDANDO CONEXOES...")

        global THREAD_ACEITAR_CONEXAO
        THREAD_ACEITAR_CONEXAO = True
        Thread(target=aceitar_conexao).start()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: servidor\nMain")
        print(erro)
