from enum import Enum
from json import dumps, loads


class TipoPedido(Enum):
    CADASTRO_USUARIO = 0
    LOGIN = 1
    ATUALIZAR_LISTA_CLIENTES = 2
    ATUALIZAR_LISTA_GRUPOS = 3
    MENSSAGEM_PRIVADA = 4
    MENSSAGEM_GRUPO = 5
    CADASTRO_GRUPO = 6
    DESCONECTAR = 7
    MENSAGEMS_PRIVADAS_ARQUIVADAS = 8
    MENSAGEMS_GRUPO_ARQUIVADAS = 9

    def to_json(self) -> str:
        return str(self.value)

    @classmethod
    def from_str(cls, string: str) -> 'TipoPedido':
        return cls(int(string))


class JSONserializable:
    def to_json(self) -> str:
        return dumps(self, default=lambda o: o.__dict__, indent=4)


class Entidade:
    def __init__(self, codigo: int, nome: str):
        self.codigo = codigo
        self.nome = nome


class Usuario(Entidade, JSONserializable):
    def to_json(self) -> str:
        self.codigo = str(self.codigo)
        return super().to_json()

    def __eq__(self, other: 'Usuario'):
        return self.codigo == other.codigo

    @classmethod
    def Usuario_from_dict(cls, dic: dict) -> 'Usuario':
        return cls(int(dic["codigo"]), dic["nome"])

    @classmethod
    def clonar(cls, usuario: 'Usuario') -> 'Usuario':
        return cls(int(usuario.codigo), usuario.nome)


class Grupo(Entidade, JSONserializable):
    def __init__(self, codigo: int, nome: str, membros: [Usuario], dono: Usuario):
        self.membros = membros
        self.dono = dono
        super().__init__(codigo, nome)

    def to_json(self) -> str:
        self.codigo = str(self.codigo)

        for indice, membro in enumerate(self.membros):
            self.membros[indice] = membro.to_json()

        self.dono = self.dono.to_json()

        return super().to_json()

    def __eq__(self, other: 'Grupo'):
        return self.codigo == other.codigo

    @classmethod
    def Grupo_from_dict(cls, dic: dict) -> 'Grupo':
        membros = []
        for membro in dic["membros"]:
            membros.append(descodificar(membro, Usuario))

        return cls(int(dic["codigo"]), dic["nome"], membros, descodificar(dic["dono"], Usuario))

    @classmethod
    def clonar(cls, grupo: 'Grupo') -> 'Grupo':
        membros = []
        for membro in grupo.membros:
            if isinstance(membro, str):
                membro = loads(membro)

            if isinstance(membro, dict):
                membro = Usuario.clonar(Usuario.Usuario_from_dict(membro))

            membros.append(Usuario.clonar(membro))

        return cls(int(grupo.codigo), grupo.nome, membros, Usuario.clonar(grupo.dono))


class Pedido(JSONserializable):
    def __init__(self, tipo: TipoPedido):
        self.tipo = tipo

    def to_json(self) -> str:
        self.tipo = self.tipo.to_json()
        return super().to_json()


class PedidoCadastroUsuario(Pedido):
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
        super().__init__(TipoPedido.CADASTRO_USUARIO)

    @classmethod
    def PedidoCadastroUsuario_from_dict(cls, dic: dict) -> 'PedidoCadastroUsuario':
        return cls(dic["nome"], dic["senha"])


class PedidoLogin(Pedido):
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
        super().__init__(TipoPedido.LOGIN)

    @classmethod
    def PedidoLogin_from_dict(cls, dic: dict) -> 'PedidoLogin':
        return cls(dic["nome"], dic["senha"])


class PedidoAtualizarListaClientes(Pedido):
    def __init__(self, remetente: Usuario):
        self.remetente = remetente
        super().__init__(TipoPedido.ATUALIZAR_LISTA_CLIENTES)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def PedidoAtualizarListaClientes_from_dict(cls, dic: dict) -> 'PedidoAtualizarListaClientes':
        return cls(descodificar(dic["remetente"], Usuario))


class PedidoAtualizarListaGrupos(Pedido):
    def __init__(self, remetente: Usuario):
        self.remetente = remetente
        super().__init__(TipoPedido.ATUALIZAR_LISTA_GRUPOS)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def PedidoAtualizarListaGrupos_from_dict(cls, dic: dict) -> 'PedidoAtualizarListaGrupos':
        return cls(descodificar(dic["remetente"], Usuario))


class PedidoCadastroGrupo(Pedido):
    def __init__(self, remetente: Usuario, nome: str, integrantes: [str]):
        self.remetente = remetente
        self.nome = nome
        self.integrantes = integrantes
        super().__init__(TipoPedido.CADASTRO_GRUPO)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def PedidoCadastroGrupo_from_dict(cls, dic: dict) -> 'PedidoCadastroGrupo':
        return cls(descodificar(dic["remetente"], Usuario), dic["nome"], dic["integrantes"])


class PedidoDesconectar(Pedido):
    def __init__(self, remetente: Usuario):
        self.remetente = remetente
        super().__init__(TipoPedido.DESCONECTAR)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def PedidoDesconectar_from_dict(cls, dic: dict) -> 'PedidoDesconectar':
        return cls(descodificar(dic["remetente"], Usuario))


class PedidoMensagensPrivadasArquivadas(Pedido):
    def __init__(self, remetente: Usuario, chat: str):
        self.remetente = remetente
        self.chat = chat
        super().__init__(TipoPedido.MENSAGEMS_PRIVADAS_ARQUIVADAS)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def PedidoMensagensPrivadasArquivadas_from_dict(cls, dic: dict) -> 'PedidoMensagensPrivadasArquivadas':
        return cls(descodificar(dic["remetente"], Usuario), dic["chat"])


class PedidoMensagensGrupoArquivadas(Pedido):
    def __init__(self, remetente: Usuario, grupo: str):
        self.remetente = remetente
        self.grupo = grupo
        super().__init__(TipoPedido.MENSAGEMS_GRUPO_ARQUIVADAS)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def PedidoMensagensGrupoArquivadas_from_dict(cls, dic: dict) -> 'PedidoMensagensGrupoArquivadas':
        return cls(descodificar(dic["remetente"], Usuario), dic["grupo"])


class MensagemPrivada(Pedido):
    def __init__(self, remetente: Usuario, mensagem: str, destinatario: str):
        self.remetente = remetente
        self.mensagem = mensagem
        self.destinatario = destinatario
        super().__init__(TipoPedido.MENSSAGEM_PRIVADA)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def MensagemPrivada_from_dict(cls, dic: dict) -> 'MensagemPrivada':
        return cls(descodificar(dic["remetente"], Usuario), dic["mensagem"], dic["destinatario"])


class MensagemGrupo(Pedido):
    def __init__(self, remetente: Usuario, mensagem: str, grupo: str):
        self.remetente = remetente
        self.mensagem = mensagem
        self.grupo = grupo
        super().__init__(TipoPedido.MENSSAGEM_GRUPO)

    def to_json(self) -> str:
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @classmethod
    def clonar(cls, mensagem_grupo: 'MensagemGrupo') -> 'MensagemGrupo':
        return cls(Usuario.clonar(mensagem_grupo.remetente), mensagem_grupo.mensagem, mensagem_grupo.grupo)

    @classmethod
    def MensagemGrupo_from_dict(cls, dic: dict) -> 'MensagemGrupo':
        return cls(descodificar(dic["remetente"], Usuario), dic["mensagem"], dic["grupo"])


def codificar(dados) -> bytes:
    if isinstance(dados, JSONserializable):
        return dados.to_json().encode()

    elif isinstance(dados, dict):
        for chave, valor in dados.items():
            if isinstance(valor, JSONserializable):
                dados[chave] = valor.to_json()
        return dumps(dados).encode()

    elif isinstance(dados, list):
        for indice, item in enumerate(dados):
            if isinstance(item, JSONserializable):
                dados[indice] = item.to_json()
        return dumps(dados).encode()

    elif isinstance(dados, str):
        return dados.encode()

    else:
        return dumps(dados).encode()


def descodificar(dados, classe):
    if isinstance(dados, bytes):
        dados = dados.decode()

    if dados is None:
        return None

    elif classe == str:
        return dados

    elif classe == int:
        return int(dados)

    elif classe == bool:
        return bool(loads(dados))

    elif classe == list:
        return list(loads(dados))

    elif classe == dict:
        return dict(loads(dados))

    elif classe == Usuario:
        dados = loads(dados)
        if dados:
            return Usuario.Usuario_from_dict(dados)
        else:
            return None

    elif classe == [Usuario]:
        dados = loads(dados)
        if dados:
            lista_usuarios = []
            for usuario in descodificar(dados, list):
                lista_usuarios.append(descodificar(usuario, Usuario))
            return lista_usuarios
        else:
            return None

    elif classe == Grupo:
        dados = loads(dados)
        if dados:
            return Grupo.Grupo_from_dict(loads(dados))
        else:
            return None

    elif classe == [Grupo]:
        dados = loads(dados)
        if dados:
            lista_grupo = []
            for grupo in descodificar(dados, list):
                lista_grupo.append(descodificar(grupo, Grupo))
            return lista_grupo
        else:
            return None

    elif classe == Pedido:
        if dados:
            dic = loads(dados)

            if dic:
                tipo = TipoPedido.from_str(dic["tipo"])

                if tipo == TipoPedido.CADASTRO_USUARIO:
                    return PedidoCadastroUsuario.PedidoCadastroUsuario_from_dict(dic)
                elif tipo == TipoPedido.LOGIN:
                    return PedidoLogin.PedidoLogin_from_dict(dic)

                elif tipo == TipoPedido.ATUALIZAR_LISTA_CLIENTES:
                    return PedidoAtualizarListaClientes.PedidoAtualizarListaClientes_from_dict(dic)

                elif tipo == TipoPedido.ATUALIZAR_LISTA_GRUPOS:
                    return PedidoAtualizarListaGrupos.PedidoAtualizarListaGrupos_from_dict(dic)

                elif tipo == TipoPedido.CADASTRO_GRUPO:
                    return PedidoCadastroGrupo.PedidoCadastroGrupo_from_dict(dic)

                elif tipo == TipoPedido.DESCONECTAR:
                    return PedidoDesconectar.PedidoDesconectar_from_dict(dic)

                elif tipo == TipoPedido.MENSAGEMS_PRIVADAS_ARQUIVADAS:
                    return PedidoMensagensPrivadasArquivadas.PedidoMensagensPrivadasArquivadas_from_dict(dic)

                elif tipo == TipoPedido.MENSAGEMS_GRUPO_ARQUIVADAS:
                    return PedidoMensagensGrupoArquivadas.PedidoMensagensGrupoArquivadas_from_dict(dic)

                elif tipo == TipoPedido.MENSSAGEM_PRIVADA:
                    return MensagemPrivada.MensagemPrivada_from_dict(dic)

                elif tipo == TipoPedido.MENSSAGEM_GRUPO:
                    return MensagemGrupo.MensagemGrupo_from_dict(dic)
            else:
                return None
        else:
            return None

    elif classe == [MensagemPrivada] or classe == [MensagemGrupo]:
        dados = loads(dados)

        if dados:
            lista_mensagens = []
            for mensagen in dados:
                lista_mensagens.append(descodificar(mensagen, Pedido))
            return lista_mensagens
        else:
            return None

    else:
        return None


# TODO delete debug function
def debug_obj_check(obj):
    print(obj, type(obj))
