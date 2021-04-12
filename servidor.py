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
            dados = conexao.recv(BUFFER)
            if dados:
                dados = dados.decode()

                dados = loads(dados)

                pedido = TipoMenssagem.converte_valor_tipo(dados["tipo"])

                if pedido == TipoMenssagem.CADASTRO:
                    resultado = debug_cadastrar(dados["nome"], dados["senha"])
                    resultado = dumps(resultado)
                    conexao.send(resultado.encode())
                    conexao.close()
                    break

                elif pedido == TipoMenssagem.LOGIN:
                    dados_cliente = debug_login(dados["nome"], dados["senha"])
                    if dados_cliente["resultado"]:
                        CLIENTES.append(DadosCliente(dados_cliente["codigo"], dados_cliente["nome"],
                                                     dados_cliente["senha"], conexao))
                    dados_cliente = dumps(dados_cliente)
                    conexao.send(dados_cliente.encode())

    # TODO too broad exception clause
    except Exception as erro_thread:
        print("Modulo: servidor\nFuncao: controlador_cliente")
        print(erro_thread)


if __name__ == "__main__":
    try:
        CLIENTES = []

        soquete = socket(AF_INET, SOCK_STREAM)
        soquete.bind((SOCKET_ENDERECO, SOCKET_PORTA))
        soquete.listen()
        print("SERVIDOR AGUARDANDO CONEXOES...")

        global THREAD_ACEITAR_CONEXAO
        THREAD_ACEITAR_CONEXAO = True
        Thread(target=aceitar_conexao).start()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: servidor\n if __name__ == '__main__'")
        print(erro)
