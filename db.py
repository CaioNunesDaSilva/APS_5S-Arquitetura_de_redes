import mysql.connector as MySQL

from auxiliar import DadosCliente
from constantes import BANCO_DE_DADOS_ENDERECO
from constantes import BANCO_DE_DADOS_NOME
from constantes import BANCO_DE_DADOS_USUARIO
from constantes import BANCO_DE_DADOS_SENHA


def __conectar(host, database, user, password):
    try:
        conexao = MySQL.connect(host=host, database=database, user=user, password=password)
        if conexao.is_connected():
            return conexao
        else:
            # TODO too broad exception clause
            raise Exception

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: db\nFuncao: conectar")
        print(erro)


def __select(conexao, campos: str, tabela: str, condicao=None):
    try:
        cursor = conexao.cursor()
        if condicao:
            cursor.execute(f"SELECT {campos} FROM {tabela} WHERE {condicao};")
        else:
            cursor.execute(f"SELECT {campos} FROM {tabela};")
        return cursor.fetchall()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: db\nFuncao: select")
        print(erro)


def __insert(conexao, tabela_campos, valores):
    try:
        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO {tabela_campos} VALUES {valores};")
        conexao.commit()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: db\nFuncao: insert")
        print(erro)


def __delete(conexao, tabela, condicao):
    try:
        cursor = conexao.cursor()
        cursor.execute(f"DELETE FROM {tabela} WHERE {condicao};")
        conexao.commit()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: db\nFuncao: delete")
        print(erro)


def __desconectar(conexao, cursor=None):
    try:
        if cursor:
            cursor.close()
        conexao.close()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: db\nFuncao: desconectar")
        print(erro)


# TODO placeholder function
def debug_cadastrar(nome: str, senha: str):
    print(nome, senha)
    return True


# TODO placeholder function
def debug_login(nome: str, senha: str):
    print(nome, senha)
    return DadosCliente("USER", "PASS", None)
