from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from json.decoder import JSONDecodeError

from auxiliar import *
from constantes import SOCKET_ENDERECO, SOCKET_PORTA, BUFFER
from db import *


def aceitar_conexao():
    while True:
        try:
            conexao, endereco = soquete.accept()
            print(f"NOVA CONEXAO: {conexao}, {endereco}")
            Thread(target=controlador_cliente, args=(conexao, endereco)).start()

        except OSError:
            print("SERVIDOR FECHADO PARA CONEXOES")
            break


def controlador_cliente(conexao, endereco):
    global CLIENTES
    global GRUPOS
    global CONEXOES
    global RECEBER_MENSAGENS_PRIVADAS
    global RECEBER_MENSAGENS_GRUPOS

    while True:
        try:
            pedido = descodificar(conexao.recv(BUFFER), Pedido)

            if pedido:

                if pedido.tipo == TipoPedido.CADASTRO_USUARIO:
                    print(f"PEDIDO DE CADASTRO DE: {pedido.nome} NA A CONEXAO {conexao}")

                    try:
                        conexao.send(codificar(cadastrar_usuario(pedido.nome, pedido.senha)))

                    except MySQL.IntegrityError:
                        print("OCORREU UM ERRO DE INTERGRIDADE NO BANCO DE DADOS")
                        conexao.send(codificar(False))

                    finally:
                        conexao.close()
                        break

                elif pedido.tipo == TipoPedido.LOGIN:
                    print(f"PEDIDO DE LOGIN DE: {pedido.nome} NA A CONEXAO {conexao}")

                    cliente = login(pedido.nome, pedido.senha)

                    if cliente:
                        CLIENTES.append(cliente)
                        CONEXOES.append(conexao)
                        RECEBER_MENSAGENS_PRIVADAS.append(False)
                        RECEBER_MENSAGENS_GRUPOS.append(False)
                        conexao.send(codificar(Usuario.clonar(cliente)))

                    else:
                        conexao.send(codificar(cliente))

                elif pedido.tipo == TipoPedido.ATUALIZAR_LISTA_CLIENTES:
                    print(f"PEDIDO DA LISTA DE USUARIOS PARA {pedido.remetente.nome} NA A CONEXAO {conexao}")

                    RECEBER_MENSAGENS_PRIVADAS[CONEXOES.index(conexao)] = False

                    lista_usuarios = []
                    for cliente in CLIENTES:
                        if cliente != pedido.remetente:
                            lista_usuarios.append(Usuario.clonar(cliente))

                    conexao.send(codificar(lista_usuarios))

                elif pedido.tipo == TipoPedido.ATUALIZAR_LISTA_GRUPOS:
                    print(f"PEDIDO DA LISTA DE GRUPOS PARA: {pedido.remetente.nome} NA A CONEXAO {conexao}")

                    RECEBER_MENSAGENS_GRUPOS[CONEXOES.index(conexao)] = False

                    lista_grupos = []
                    for grupo in GRUPOS:
                        if pedido.remetente in grupo.membros:
                            lista_grupos.append(Grupo.clonar(grupo))

                    conexao.send(codificar(lista_grupos))

                elif pedido.tipo == TipoPedido.MENSSAGEM_PRIVADA:
                    print(f"TROCA DE MENSAGENS ENTRE {pedido.remetente.nome} E"
                          f" {pedido.destinatario} NA CONEXAO {conexao}")

                    for indice, cliente in enumerate(CLIENTES):
                        if pedido.destinatario == cliente.nome:
                            if RECEBER_MENSAGENS_PRIVADAS[indice]:
                                pedido = codificar(pedido)
                                CONEXOES[indice].send(pedido)
                                conexao.send(pedido)
                            else:
                                print(f"MENSAGENS ARQUIVADA PARA DE {pedido.remetente} PARA {pedido.destinatario}"
                                      f" NA CONEXAO {conexao}")
                                conexao.send(codificar(MensagemPrivada(Usuario(0, "Servidor"),
                                                                       "Usuario não esta disponivel",
                                                                       pedido.remetente.nome)))
                                arquivar_mensagens_privadas(pedido)

                            break

                    else:
                        conexao.send(codificar(MensagemPrivada(Usuario(0, "Servidor"),
                                                               "Usuario se desconectou",
                                                               pedido.remetente.nome)))

                elif pedido.tipo == TipoPedido.MENSSAGEM_GRUPO:
                    print(f"MENSAGENS DE {pedido.remetente.nome} NO GRUPO {pedido.grupo} NA CONEXAO {conexao}")

                    usuarios_nao_disponiveis = []
                    for grupo in GRUPOS:
                        if grupo.nome == pedido.grupo:
                            for cliente in grupo.membros:
                                if cliente in CLIENTES and RECEBER_MENSAGENS_GRUPOS[CLIENTES.index(cliente)]:
                                    CONEXOES[CLIENTES.index(cliente)].send(codificar(MensagemGrupo.clonar(pedido)))
                                else:
                                    usuarios_nao_disponiveis.append(cliente)

                            if usuarios_nao_disponiveis:
                                print(f"MENSAGENS ARQUIVADA PARA ALGUNS USUARIOS NO GRUPO {pedido.grupo}"
                                      f" MA CONEXAO {conexao}")
                                arquivar_mensagens_grupo(pedido, usuarios_nao_disponiveis)

                            break

                elif pedido.tipo == TipoPedido.CADASTRO_GRUPO:
                    print(f"PEDIDO DE CADASTRO DE GRUPO POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                    conexao.send(codificar(cadastrar_grupo(pedido.nome, pedido.integrantes, pedido.remetente)))
                    GRUPOS = carregar_grupos()

                elif pedido.tipo == TipoPedido.DESCONECTAR:
                    print(f"PEDIDO DE DESCONEXAO POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                    for indice, cliente in enumerate(CLIENTES):
                        if pedido.remetente == cliente:
                            CLIENTES.pop(indice)
                            CONEXOES.pop(indice)
                            RECEBER_MENSAGENS_PRIVADAS.pop(indice)
                            RECEBER_MENSAGENS_GRUPOS.pop(indice)

                    conexao.close()
                    break

                elif pedido.tipo == TipoPedido.MENSAGEMS_PRIVADAS_ARQUIVADAS:
                    print(f"PEDIDO DE ENVIO DE MENSAGENS PRIVADAS ARQUIVADAS"
                          f" POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                    RECEBER_MENSAGENS_PRIVADAS[CONEXOES.index(conexao)] = True

                    conexao.send(codificar(mensagens_privadas_arquivadas(pedido.chat, pedido.remetente.nome)))

                elif pedido.tipo == TipoPedido.MENSAGEMS_GRUPO_ARQUIVADAS:
                    print(f"PEDIDO DE ENVIO DE MENSAGENS DE GRUPO ARQUIVADAS"
                          f" POR {pedido.remetente.nome} NA CONEXAO {conexao}")

                    RECEBER_MENSAGENS_GRUPOS[CONEXOES.index(conexao)] = True

                    conexao.send(codificar(mensagens_grupo_arquivadas(pedido.grupo, pedido.remetente.nome)))

            else:
                conexao.send(codificar(None))

        except ConnectionAbortedError:
            print(f"CONEXAO {conexao} ABORTADA DEVIDO A FALTA DE RESPOSTA")
            try:
                CLIENTES.pop(CONEXOES.index(conexao))
                CONEXOES.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_PRIVADAS.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_GRUPOS.pop(CONEXOES.index(conexao))
            except ValueError:
                pass
            conexao.close()
            break

        except ConnectionResetError:
            print(f"CONEXAO {conexao} FOI FECHADA ABRUPTAMENTE")
            try:
                CLIENTES.pop(CONEXOES.index(conexao))
                CONEXOES.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_PRIVADAS.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_GRUPOS.pop(CONEXOES.index(conexao))
            except ValueError:
                pass
            conexao.close()
            break

        except OSError:
            print(f"ERRO DE CONEXAO NO SOQUETE NA CONEXAO {conexao}")
            try:
                CLIENTES.pop(CONEXOES.index(conexao))
                CONEXOES.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_PRIVADAS.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_GRUPOS.pop(CONEXOES.index(conexao))
            except ValueError:
                pass
            conexao.close()
            break

        except JSONDecodeError:
            print(f"DADOS INVALIDOS RECEBIDOS NA CONEXAO {conexao}")
            try:
                CLIENTES.pop(CONEXOES.index(conexao))
                CONEXOES.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_PRIVADAS.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_GRUPOS.pop(CONEXOES.index(conexao))
            except ValueError:
                pass
            conexao.close()
            break

        except AttributeError:
            print(f"DADOS EM FORMATO INVALIDO ENCONTRADOS NA CONEXAO {conexao}")
            try:
                CLIENTES.pop(CONEXOES.index(conexao))
                CONEXOES.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_PRIVADAS.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_GRUPOS.pop(CONEXOES.index(conexao))
            except ValueError:
                pass
            try:
                conexao.close()
            except AttributeError:
                pass
            break

        except (MySQL.ProgrammingError, MySQL.IntegrityError, MySQL.DatabaseError):
            print(f"TABELA DO BANCO DE DADOS EM FORMATO DIFERENTE DO ESPERADO")
            try:
                CLIENTES.pop(CONEXOES.index(conexao))
                CONEXOES.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_PRIVADAS.pop(CONEXOES.index(conexao))
                RECEBER_MENSAGENS_GRUPOS.pop(CONEXOES.index(conexao))
            except ValueError:
                pass
            try:
                conexao.close()
            except AttributeError:
                pass
            break


if __name__ == "__main__":
    try:
        CLIENTES = []
        CONEXOES = []
        RECEBER_MENSAGENS_PRIVADAS = []
        RECEBER_MENSAGENS_GRUPOS = []
        GRUPOS = carregar_grupos()

        soquete = socket(AF_INET, SOCK_STREAM)
        soquete.bind((SOCKET_ENDERECO, SOCKET_PORTA))
        soquete.listen()

        thread_aceitar_conexao = Thread(target=aceitar_conexao)
        thread_aceitar_conexao.start()
        print("SERVIDOR AGUARDANDO CONEXOES...")

    except MySQL.InterfaceError:
        print("NAO FOI POSSIVEL SE CONECTAR AO BANCO DE DADOS")
        try:
            soquete.close()
        except NameError:
            pass
        exit()

    except MySQL.ProgrammingError:
        print("BANCO DE DADOS FORA DOS PADROES")
        try:
            soquete.close()
        except NameError:
            pass
        exit()

    except Exception as erro:
        print(f"OCORREU O ERRO {erro}, REINICIE O SERVIDOR")
        try:
            soquete.close()
        except NameError:
            pass
        exit()

    try:
        while True:
            comando = input("SERVIDOR ACEITANDO COMANDOS...\n")

            if comando.upper() == "SAIR":
                soquete.close()
                exit()
                print("AINDA A USUARIOS CONECTADOS, AGUARDE...")

            elif comando.upper() == "FECHAR":
                soquete.close()

            elif comando.upper() == "ABRIR":
                if not thread_aceitar_conexao.is_alive():
                    soquete = socket(AF_INET, SOCK_STREAM)
                    soquete.bind((SOCKET_ENDERECO, SOCKET_PORTA))
                    soquete.listen()

                    thread_aceitar_conexao = Thread(target=aceitar_conexao)
                    thread_aceitar_conexao.start()
                    print("SERVIDOR AGUARDANDO CONEXOES...")

                else:
                    print("SERVIDOR JA ESTA ABERTO A CONEXOES")

            else:
                print("COMANDO INVALIDO")

    except OSError:
        print("OCORREU UM ERRO NO SOQUETE")
        try:
            soquete.close()
        except AttributeError:
            pass

    except Exception as erro:
        print(f"OCORREU O ERRO {erro}, REINICIE O SERVIDOR")
        try:
            soquete.close()
        except AttributeError:
            pass
