from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from threading import Thread

from auxiliar import *
from constantes import SOCKET_ENDERECO
from constantes import SOCKET_PORTA
from constantes import BUFFER
from db import debug_cadastrar
from db import debug_login
from db import debug_carregar_grupos


def aceitar_conexao():
    while THREAD_ACEITAR_CONEXAO:
        conexao, endereco = soquete.accept()
        print(f"NOVA CONEXAO: {conexao}, {endereco}")
        Thread(target=controlador_cliente, args=(conexao, endereco)).start()


def controlador_cliente(conexao, endereco):
    while True:
        pedido = conexao.recv(BUFFER)

        if pedido:

            pedido = descodificar(pedido)
            tipo = TipoPedido.from_str(pedido["tipo"])

            if tipo == TipoPedido.CADASTRO_USUARIO:
                pedido = PedidoCadastroUsuario.PedidoCadastroUsuario_from_dict(pedido)

                conexao.send(codificar(debug_cadastrar(pedido.nome, pedido.senha)))
                conexao.close()
                break

            elif tipo == TipoPedido.LOGIN:
                pedido = PedidoLogin.PedidoLogin_from_dict(pedido)

                cliente = debug_login(pedido.nome, pedido.senha)

                if cliente:
                    CLIENTES.append(cliente)

                conexao.send(codificar(cliente))

            elif tipo == TipoPedido.ATUALIZAR_LISTA_CLIENTES:
                pedido = PedidoAtualizarListaClientes.PedidoAtualizarListaClientes_from_dict(pedido)

                lista_usuarios = []
                for cliente in CLIENTES:
                    if cliente != pedido.remetente:
                        lista_usuarios.append(cliente)

                conexao.send(codificar(lista_usuarios))


if __name__ == "__main__":
    CLIENTES = []
    GRUPOS = debug_carregar_grupos()

    soquete = socket(AF_INET, SOCK_STREAM)
    soquete.bind((SOCKET_ENDERECO, SOCKET_PORTA))
    soquete.listen()
    print("SERVIDOR AGUARDANDO CONEXOES...")

    THREAD_ACEITAR_CONEXAO = True
    Thread(target=aceitar_conexao).start()
