from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from threading import Thread

from auxiliar import *
from constantes import SOCKET_ENDERECO
from constantes import SOCKET_PORTA
from constantes import BUFFER
from db import *


def aceitar_conexao():
    while THREAD_ACEITAR_CONEXAO:
        conexao, endereco = soquete.accept()
        print(f"NOVA CONEXAO: {conexao}, {endereco}")
        Thread(target=controlador_cliente, args=(conexao, endereco)).start()


def controlador_cliente(conexao, endereco):
    global GRUPOS

    while True:
        pedido = descodificar(conexao.recv(BUFFER), Pedido)

        if pedido:

            if pedido.tipo == TipoPedido.CADASTRO_USUARIO:
                print(f"PEDIDO DE CADASTRO DE: {pedido.nome} NA A CONEXAO {conexao}")

                conexao.send(codificar(debug_cadastrar(pedido.nome, pedido.senha)))
                conexao.close()
                break

            elif pedido.tipo == TipoPedido.LOGIN:
                print(f"PEDIDO DE LOGIN DE: {pedido.nome} NA A CONEXAO {conexao}")

                cliente = debug_login(pedido.nome, pedido.senha)

                if cliente:
                    CLIENTES.append([cliente, conexao])

                conexao.send(codificar(Usuario.clonar(cliente)))

            elif pedido.tipo == TipoPedido.ATUALIZAR_LISTA_CLIENTES:
                print(f"PEDIDO DA LISTA DE USUARIOS PARA {pedido.remetente.nome} NA A CONEXAO {conexao}")

                lista_usuarios = []
                for cliente, soquete_cliente in CLIENTES:
                    if cliente != pedido.remetente:
                        lista_usuarios.append(Usuario.clonar(cliente))

                conexao.send(codificar(lista_usuarios))

            elif pedido.tipo == TipoPedido.ATUALIZAR_LISTA_GRUPOS:
                print(f"PEDIDO DA LISTA DE GRUPOS PARA: {pedido.remetente.nome} NA A CONEXAO {conexao}")

                lista_grupos = []
                for grupo in GRUPOS:
                    if pedido.remetente in grupo.membros:
                        lista_grupos.append(Grupo.clonar(grupo))

                conexao.send(codificar(lista_grupos))

            elif pedido.tipo == TipoPedido.MENSSAGEM_PRIVADA:
                print(f"TROCA DE MENSAGENS ENTRE {pedido.remetente.nome} E {pedido.destinatario} NA CONEXAO {conexao}")

                for cliente, soquete_cliente in CLIENTES:
                    if pedido.destinatario == cliente.nome:
                        soquete_cliente.send(codificar(pedido))

            elif pedido.tipo == TipoPedido.MENSSAGEM_GRUPO:
                print(f"MENSAGENS DE {pedido.remetente.nome} NO GRUPO {pedido.grupo} NA CONEXAO {conexao}")

                for grupo in GRUPOS:
                    if grupo.nome == pedido.grupo:
                        for cliente, soquete_cliente in CLIENTES:
                            if cliente in grupo.membros and cliente != pedido.remetente:
                                soquete_cliente.send(codificar(MensagemGrupo.clonar(pedido)))
                        break

            elif pedido.tipo == TipoPedido.CADASTRO_GRUPO:
                print(f"PEDIDO DE CADASTRO DE GRUPO POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                conexao.send(codificar(debug_cadastrar_grupo(pedido.nome, pedido.integrantes)))
                GRUPOS = debug_carregar_grupos()

            elif pedido.tipo == TipoPedido.DESCONECTAR:
                print(f"PEDIDO DE DESCONEXAO POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                usuario_desconetado = None
                for indice, cliente in enumerate(CLIENTES):
                    if pedido.remetente == cliente[0]:
                        usuario_desconetado = CLIENTES.pop(indice)

                conexao.send(codificar(bool(usuario_desconetado)))

                conexao.close()
                break

            elif pedido.tipo == TipoPedido.MENSAGEMS_PRIVADAS_ARQUIVADAS:
                print(f"PEDIDO DE ENVIO DE MENSAGENS PRIVADAS ARQUIVADAS POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                conexao.send(codificar(debug_mensagens_privadas_arquivadas(pedido.chat, pedido.remetente.nome)))

            elif pedido.tipo == TipoPedido.MENSAGEMS_GRUPO_ARQUIVADAS:
                print(f"PEDIDO DE ENVIO DE MENSAGENS DE GRUPO ARQUIVADAS POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                conexao.send(codificar(debug_mensagens_grupo_arquivadas(pedido.grupo, pedido.remetente.nome)))

        else:
            conexao.send(codificar(None))


if __name__ == "__main__":
    # TODO deletar valores de teste
    CLIENTES = [[Usuario(0, "teste1"), None],
                [Usuario(0, "teste2"), None]]
    GRUPOS = debug_carregar_grupos()

    soquete = socket(AF_INET, SOCK_STREAM)
    soquete.bind((SOCKET_ENDERECO, SOCKET_PORTA))
    soquete.listen()
    print("SERVIDOR AGUARDANDO CONEXOES...")

    THREAD_ACEITAR_CONEXAO = True
    Thread(target=aceitar_conexao).start()
