from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from threading import Thread
from json import loads
from json import dumps

from auxiliar import TipoMenssagem
from constantes import SOCKET_ENDERECO
from constantes import SOCKET_PORTA
from constantes import BUFFER
from db import debug_cadastrar



def aceitar_conexao():
    while THREAD_ACEITAR_CONEXAO:
        conexao, endereco = soquete.accept()
        print(f"NOVA CONEXAO: {conexao}, {endereco}")
        Thread(target=controlador_cliente, args=(conexao, endereco)).start()


def controlador_cliente(conexao, endereco):
    while True:
        dados = conexao.recv(BUFFER).decode()
        dados = loads(dados)

        if TipoMenssagem.converte_valor_tipo(dados["tipo"] == TipoMenssagem.CADASTRO):
            resultado = debug_cadastrar(dados["nome"], dados["senha"])
            resultado = dumps(resultado)
            conexao.send(resultado.encode())
            conexao.close()
            break


if __name__ == "__main__":
    soquete = socket(AF_INET, SOCK_STREAM)
    soquete.bind((SOCKET_ENDERECO, SOCKET_PORTA))
    soquete.listen()
    print("SERVIDOR AGUARDANDO CONEXOES...")

    global THREAD_ACEITAR_CONEXAO
    THREAD_ACEITAR_CONEXAO = True
    Thread(target=aceitar_conexao).start()
