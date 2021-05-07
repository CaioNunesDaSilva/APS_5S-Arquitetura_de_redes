import mysql.connector as MySQL

from auxiliar import Usuario
from auxiliar import Grupo
from auxiliar import MensagemPrivada
from auxiliar import MensagemGrupo
from constantes import BANCO_DE_DADOS_ENDERECO
from constantes import BANCO_DE_DADOS_NOME
from constantes import BANCO_DE_DADOS_USUARIO
from constantes import BANCO_DE_DADOS_SENHA


def __conectar(host, database, user, password):
    conexao = MySQL.connect(host=host, database=database, user=user, password=password)
    if conexao.is_connected():
        return conexao


def __select(conexao, campos: str, tabela: str, condicao=None):
    cursor = conexao.cursor()
    if condicao:
        cursor.execute(f"SELECT {campos} FROM {tabela} WHERE {condicao};")
    else:
        cursor.execute(f"SELECT {campos} FROM {tabela};")
    return cursor.fetchall()


def __insert(conexao, tabela_campos, valores):
    cursor = conexao.cursor()
    cursor.execute(f"INSERT INTO {tabela_campos} VALUES {valores};")
    conexao.commit()


def __delete(conexao, tabela, condicao):
    cursor = conexao.cursor()
    cursor.execute(f"DELETE FROM {tabela} WHERE {condicao};")
    conexao.commit()


def __desconectar(conexao, cursor=None):
    if cursor:
        cursor.close()
    conexao.close()


# TODO deletar funcao de debug
def debug_cadastrar(nome: str, senha: str):
    return True


# TODO deletar funcao de debug
def debug_cadastrar_grupo(nome: str, integrantes):
    return True


# TODO deletar funcao de debug
def debug_login(nome: str, senha: str):
    return Usuario(1, nome)


# TODO deletar funcao de debug
def debug_carregar_grupos():
    return [Grupo(1, "grupo1", [Usuario(1, "a"), Usuario(2, "b")], Usuario(1, "a")),
            Grupo(2, "grupo2", [Usuario(1, "a")], Usuario(1, "a"))]


# TODO deletar funcao de debug
def debug_mensagens_privadas_arquivadas(chat: str, destinatario: str):
    if chat == "teste1" and destinatario == "a":
        return [MensagemPrivada(Usuario(0, "teste1"), "hello", "a"), MensagemPrivada(Usuario(0, "teste1"), "world", "a")]


# TODO deletar funcao de debug
def debug_mensagens_grupo_arquivadas(grupo: str, usuario: str):
    if grupo == "grupo1" and usuario == "a":
        return [MensagemGrupo(Usuario(0, "teste1"), "hello", "grupo1"), MensagemGrupo(Usuario(0, "teste2"), "world", "grupo1")]

