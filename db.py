import mysql.connector as MySQL

from auxiliar import Usuario
from auxiliar import Grupo
from auxiliar import MensagemPrivada
from auxiliar import MensagemGrupo
from constantes import BANCO_DE_DADOS_ENDERECO
from constantes import BANCO_DE_DADOS_NOME
from constantes import BANCO_DE_DADOS_USUARIO
from constantes import BANCO_DE_DADOS_SENHA


def __conectar(host=BANCO_DE_DADOS_ENDERECO, database=BANCO_DE_DADOS_NOME,
               user=BANCO_DE_DADOS_USUARIO, password=BANCO_DE_DADOS_SENHA) -> MySQL.MySQLConnection:
    conexao = MySQL.connect(host=host, database=database, user=user, password=password)
    if conexao.is_connected():
        return conexao


def __select(conexao: MySQL.MySQLConnection, campos: str, tabela: str, condicao=None):
    cursor = conexao.cursor()
    if condicao:
        cursor.execute(f"SELECT {campos} FROM {tabela} WHERE {condicao};")
    else:
        cursor.execute(f"SELECT {campos} FROM {tabela};")
    selecao = cursor.fetchall()

    if isinstance(selecao, tuple):
        lista = []
        for linha in selecao:
            lista.append(linha)
        selecao = lista

    for indice, linha in enumerate(selecao):
        if isinstance(linha, tuple):
            if len(linha) < 1:
                selecao.pop(indice)
            elif len(linha) == 1:
                selecao[indice] = linha[0]

    if len(selecao) == 1:
        if isinstance(selecao[0], tuple):
            lista = []
            for linha in selecao[0]:
                lista.append(linha)
            selecao = lista
        else:
            selecao = selecao[0]

    return selecao


def __insert(conexao: MySQL.MySQLConnection, tabela_campos: str, valores: tuple):
    cursor = conexao.cursor()
    cursor.execute(f"INSERT INTO {tabela_campos} VALUES {valores};")


def __update(conexao: MySQL.MySQLConnection, tabela: str, coluna_valor: str, condicao: str):
    cursor = conexao.cursor()
    cursor.execute(f"UPDATE {tabela} SET {coluna_valor} WHERE {condicao};")


def __delete(conexao: MySQL.MySQLConnection, tabela: str, condicao: str):
    cursor = conexao.cursor()
    cursor.execute(f"DELETE FROM {tabela} WHERE {condicao};")


def __desconectar(conexao: MySQL.MySQLConnection, cursor=None, rollback=False):
    if rollback:
        conexao.rollback()
    else:
        conexao.commit()
    if cursor:
        cursor.close()
    conexao.close()


def cadastrar_usuario(nome: str, senha: str) -> bool:
    conexao = __conectar()
    dados = __select(conexao, "nm_usuario, cd_senha", "usuarios")
    if (nome, senha) in dados:
        __desconectar(conexao)
        return False
    else:
        __insert(conexao, "usuarios (nm_usuario, cd_senha)", (nome, senha))
        __desconectar(conexao)
        return True


def cadastrar_grupo(nome: str, integrantes: [str], dono: Usuario) -> bool:
    integrantes.append(dono.nome)
    conexao = __conectar()
    dados = __select(conexao, "nm_grupo", "grupos")
    if nome in dados:
        __desconectar(conexao)
        return False
    else:
        __insert(conexao, "grupos(nm_grupo, cd_dono)", (nome, dono.codigo))
        dados = __select(conexao, "cd_grupo", "grupos", f"nm_grupo='{nome}'")
        if dados:
            for nome_integrante in integrantes:
                codigo_integrante = __select(conexao, "cd_usuario", "usuarios", f"nm_usuario='{nome_integrante}'")
                __insert(conexao, "membros_grupo(fk_usuario, fk_grupo)", (codigo_integrante, dados))
                check = __select(conexao, "*", "membros_grupo",
                                 f"fk_usuario={codigo_integrante} and fk_grupo={dados}")
                if not check:
                    __desconectar(conexao, rollback=True)
                    raise MySQL.Error("insert nao executado")

                __desconectar(conexao)
                return True

        else:
            __desconectar(conexao, rollback=True)
            raise MySQL.Error("insert nao executado")


def login(nome: str, senha: str) -> Usuario:
    conexao = __conectar()
    dados_usuario = __select(conexao, "cd_usuario, nm_usuario", "usuarios",
                             f"nm_usuario='{nome}' and cd_senha='{senha}'")
    if dados_usuario:
        __desconectar(conexao)
        return Usuario(dados_usuario[0], dados_usuario[1])
    else:
        __desconectar(conexao)
        return None


def carregar_grupos() -> [Grupo]:
    lista_grupos = []
    conexao = __conectar()
    dados_grupos = __select(conexao, "cd_grupo, nm_grupo, cd_dono", "grupos")
    if dados_grupos:
        for dados_grupo in dados_grupos:
            dados_dono = __select(conexao, "cd_usuario, nm_usuario", "usuarios", f"cd_usuario='{dados_grupo[2]}'")
            dono = Usuario(dados_dono[0], dados_dono[1])
            lista_membros = []
            codigos_membros = __select(conexao, "fk_usuario", "membros_grupo", f"fk_grupo={dados_grupo[0]}")
            for codigo_membro in codigos_membros:
                dados_membro = __select(conexao, "cd_usuario, nm_usuario", "usuario", f"cd_usuario={codigo_membro}")
                lista_membros.append(Usuario(dados_membro[0], dados_membro[1]))
            lista_grupos.append(Grupo(dados_grupo[0], dados_grupo[1], lista_membros, dono))
    __desconectar(conexao)
    return lista_grupos


def mensagens_privadas_arquivadas(remetente_chat: str, destinatario_chat: str) -> [MensagemPrivada]:
    lista_mensagens = []
    conexao = __conectar()
    codigo_remetente_chat = __select(conexao, "cd_usuario", "usuarios", f"nm_usuario='{remetente_chat}'")
    codigo_destinatario_chat = __select(conexao, "cd_usuario", "usuarios", f"nm_usuario='{destinatario_chat}'")
    dados_mensagens = __select(conexao, "cd_mensagem, ds_mensagem", "mensagens_privadas",
                               f"fk_remetente={codigo_remetente_chat} and fk_destinatario={codigo_destinatario_chat}"
                               f" and bl_recibido=0")
    for dados_mensagem in dados_mensagens:
        lista_mensagens.append(MensagemPrivada(Usuario(codigo_remetente_chat, remetente_chat),
                                               dados_mensagem[1], destinatario_chat))
        __update(conexao, "mensagens_privadas", "bl_recebido=1", f"cd_mensagem_privada={dados_mensagem[0]}")

    __desconectar(conexao)
    return lista_mensagens


def mensagens_grupo_arquivadas(grupo: str, destinatario_chat: str) -> [MensagemGrupo]:
    lista_mensagens = []
    conexao = __conectar()
    codigo_grupo = __select(conexao, "cd_grupos", "grupos", f"nm_grupo='{grupo}'")
    codigo_destinatario_chat = __select(conexao, "cd_usuario", "usuarios", f"nm_usuario='{destinatario_chat}'")
    dados_mensagens = __select(conexao, "cd_mensagem_grupo, fk_usuario, ds_mensagem",
                               "mensagens_grupo JOIN mensagem_grupo_recebido"
                               " ON mensagens_grupo.cd_mensagem_grupo = mensagem_grupo_recebido.fk_mensagem_grupo",
                               f"mensagens_grupo.fk_grupo={codigo_grupo} and"
                               f" mensagem_grupo_recebido.fk_usuario={codigo_destinatario_chat} and "
                               f"mensagem_grupo_recebido.bl_recebido=0")
    for dados_mensagem in dados_mensagens:
        nome_remtente_chat = __select(conexao, "nm_usuario", "usuarios", f"cd_usuario={dados_mensagem[1]}")
        lista_mensagens.append(MensagemGrupo(Usuario(dados_mensagem[1], nome_remtente_chat),
                                             dados_mensagem[2], destinatario_chat))
        __update(conexao, "mensagem_grupo_recebido", "bl_recebido=1",
                 f"fk_mensagem_grupo={dados_mensagem[0]} and fk_usuario={codigo_destinatario_chat}")

    __desconectar(conexao)
    return lista_mensagens


def arquivar_mensagens_privadas(mensagem: MensagemPrivada):
    conexao = __conectar()
    destinatario_codigo = __select(conexao, "cd_usuario", "usuarios", f"nm_usuario='{mensagem.destinatario}'")
    __insert(conexao, "mensagens_privadas (fk_remetente, fk_destinatario, ds_mensagem, bl_recebido)",
             (mensagem.remetente.codigo, destinatario_codigo, mensagem.mensagem, 0))
    __desconectar(conexao)


def arquivar_mensagens_grupo(mensagem: MensagemGrupo, usuarios_nao_disponiveis: [Usuario]):
    conexao = __conectar()
    codigo_grupo = __select(conexao, "cd_grupo", "grupos", f"nm_grupo='{mensagem.grupo}'")
    __insert(conexao, "mensagens_grupo (fk_usuario, fk_grupo, ds_mensagem)",
             (mensagem.remetente.codigo, codigo_grupo, mensagem.mensagem))
    codigo_mensagem = __select(conexao, "cd_mensagem", "mensagens_grupo",
                               f"fk_usuario={mensagem.remetente.codigo} and "
                               f"fk_grupo={codigo_grupo} and "
                               f"ds_mensagem='{mensagem.mensagem}'")
    if codigo_mensagem:
        for usuario_nao_disponivel in usuarios_nao_disponiveis:
            codigo_usuario_nao_disponivel = __select(conexao, "cd_usuario", "usuarios",
                                                     f"nm_usuario='{usuario_nao_disponivel.nome}'")
            __insert(conexao, "mensagem_grupo_recebido (fk_mensagem_grupo, fk_usuario, bl_recebido)",
                     (codigo_mensagem, codigo_usuario_nao_disponivel, 0))
            check = __select(conexao, "*", "mensagem_grupo_recebido",
                             f"fk_mensagem_grupo={codigo_mensagem} and fk_usuario={codigo_usuario_nao_disponivel}")
            if not check:
                __desconectar(conexao, rollback=True)
                raise MySQL.Error("insert nao executado")

    else:
        __desconectar(conexao, rollback=True)
        raise MySQL.Error("insert nao executado")
