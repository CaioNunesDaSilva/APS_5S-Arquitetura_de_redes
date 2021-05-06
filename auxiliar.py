from enum import Enum
from json import dumps
from json import loads


class TipoPedido(Enum):
    CADASTRO_USUARIO = 0
    LOGIN = 1
    ATUALIZAR_LISTA_CLIENTES = 2
    ATUALIZAR_LISTA_GRUPOS = 3
    MENSSAGEM_PRIVADA = 4
    MENSSAGEM_GRUPO = 5
    CADASTRO_GRUPO = 6
    DESCONECTAR = 7

    def to_json(self):
        return str(self.value)

    @staticmethod
    def from_str(string: str):
        return TipoPedido(int(string))


class JSONserializable:
    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class ObjetoDB:
    def __init__(self, codigo: int, nome: str, ):
        self.codigo = codigo
        self.nome = nome


class Usuario(ObjetoDB, JSONserializable):
    def __init__(self, codigo: int, nome: str):
        super().__init__(codigo, nome)

    def to_json(self):
        self.codigo = str(self.codigo)
        return super().to_json()

    def __eq__(self, other):
        return self.nome == other.nome

    @staticmethod
    def Usuario_from_dict(dic):
        return Usuario(int(dic["codigo"]), dic["nome"])

    @staticmethod
    def clonar(obj):
        return Usuario(obj.codigo, obj.nome)


class Grupo(ObjetoDB, JSONserializable):
    def __init__(self, codigo: int, nome: str, membros: [Usuario], dono: Usuario):
        self.membros = membros
        self.dono = dono
        super().__init__(codigo, nome)

    def to_json(self):
        self.codigo = str(self.codigo)

        for indice, membro in enumerate(self.membros):
            self.membros[indice] = membro.to_json()

        self.dono = self.dono.to_json()

        return super().to_json()

    def __eq__(self, other):
        return self.nome == other.nome

    @staticmethod
    def Grupo_from_dict(dic):
        membros = []
        for membro in dic["membros"]:
            membros.append(Usuario.Usuario_from_dict(descodificar(membro)))

        return Grupo(dic["codigo"], dic["nome"], membros, Usuario.Usuario_from_dict(descodificar(dic["dono"])))

    @staticmethod
    def clonar(obj):
        membros = []
        for membro in obj.membros:
            if isinstance(membro, str):
                membro = loads(membro)

            if isinstance(membro, dict):
                membro = Usuario.Usuario_from_dict(membro)

            membros.append(Usuario.clonar(membro))

        return Grupo(obj.codigo, obj.nome, membros, Usuario.clonar(obj.dono))


class Pedido(JSONserializable):
    def __init__(self, tipo: TipoPedido):
        self.tipo = tipo

    def to_json(self):
        self.tipo = self.tipo.to_json()
        return super().to_json()


class PedidoCadastroUsuario(Pedido):
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
        super().__init__(TipoPedido.CADASTRO_USUARIO)

    @staticmethod
    def PedidoCadastroUsuario_from_dict(dic):
        return PedidoCadastroUsuario(dic["nome"], dic["senha"])


class PedidoLogin(Pedido):
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
        super().__init__(TipoPedido.LOGIN)

    @staticmethod
    def PedidoLogin_from_dict(dic):
        return PedidoLogin(dic["nome"], dic["senha"])


class PedidoAtualizarListaClientes(Pedido):
    def __init__(self, remetente: Usuario):
        self.remetente = remetente
        super().__init__(TipoPedido.ATUALIZAR_LISTA_CLIENTES)

    def to_json(self):
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @staticmethod
    def PedidoAtualizarListaClientes_from_dict(dic):
        return PedidoAtualizarListaClientes(Usuario.Usuario_from_dict(descodificar(dic["remetente"])))


class PedidoAtualizarListaGrupos(Pedido):
    def __init__(self, remetente: Usuario):
        self.remetente = remetente
        super().__init__(TipoPedido.ATUALIZAR_LISTA_GRUPOS)

    def to_json(self):
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @staticmethod
    def PedidoAtualizarListaGrupos_from_dict(dic):
        return PedidoAtualizarListaGrupos(Usuario.Usuario_from_dict(descodificar(dic["remetente"])))


class MensagemPrivada(Pedido):
    def __init__(self, remetente: Usuario, mensagem: str, destinatario: str):
        self.remetente = remetente
        self.mensagem = mensagem
        self.destinatario = destinatario
        super().__init__(TipoPedido.MENSSAGEM_PRIVADA)

    def to_json(self):
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @staticmethod
    def MensagemPrivada_from_dict(dic):
        return MensagemPrivada(Usuario.Usuario_from_dict(descodificar(dic["remetente"])),
                               dic["mensagem"],
                               dic["destinatario"])


class MensagemGrupo(Pedido):
    def __init__(self, remetente: Usuario, mensagem: str, grupo: str):
        self.remetente = remetente
        self.mensagem = mensagem
        self.grupo = grupo
        super().__init__(TipoPedido.MENSSAGEM_GRUPO)

    def to_json(self):
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @staticmethod
    def clonar(obj):
        return MensagemGrupo(obj.remetente, obj.mensagem, obj.grupo)

    @staticmethod
    def MensagemGrupo_from_dict(dic):
        return MensagemGrupo(Usuario.Usuario_from_dict(descodificar(dic["remetente"])),
                             dic["mensagem"],
                             dic["grupo"])


class PedidoCadastroGrupo(Pedido):
    def __init__(self, remetente: Usuario, nome: str, integrantes):
        self.remetente = remetente
        self.nome = nome
        self.integrantes = integrantes
        super().__init__(TipoPedido.CADASTRO_GRUPO)

    def to_json(self):
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @staticmethod
    def PedidoCadastroGrupo_from_dict(dic):
        return PedidoCadastroGrupo(Usuario.Usuario_from_dict(descodificar(dic["remetente"])),
                                   dic["nome"],
                                   dic["integrantes"])


class PedidoDesconectar(Pedido):
    def __init__(self, remetente: Usuario):
        self.remetente = remetente
        super().__init__(TipoPedido.DESCONECTAR)

    def to_json(self):
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @staticmethod
    def PedidoDesconectar_from_dict(dic):
        return PedidoDesconectar(Usuario.Usuario_from_dict(descodificar(dic["remetente"])))


def Pedido_from_dic(dic: dict):
    if isinstance(dic, str):
        dic = loads(dic)

    tipo = TipoPedido.from_str(dic["tipo"])
    if tipo == TipoPedido.CADASTRO_USUARIO:
        return PedidoCadastroUsuario.PedidoCadastroUsuario_from_dict(dic)
    elif tipo == TipoPedido.LOGIN:
        return PedidoLogin.PedidoLogin_from_dict(dic)
    elif tipo == TipoPedido.ATUALIZAR_LISTA_CLIENTES:
        return PedidoAtualizarListaClientes.PedidoAtualizarListaClientes_from_dict(dic)
    elif tipo == TipoPedido.ATUALIZAR_LISTA_GRUPOS:
        return PedidoAtualizarListaGrupos.PedidoAtualizarListaGrupos_from_dict(dic)
    elif tipo == TipoPedido.MENSSAGEM_PRIVADA:
        return MensagemPrivada.MensagemPrivada_from_dict(dic)
    elif tipo == TipoPedido.MENSSAGEM_GRUPO:
        return MensagemGrupo.MensagemGrupo_from_dict(dic)
    elif tipo == TipoPedido.CADASTRO_GRUPO:
        return PedidoCadastroGrupo.PedidoCadastroGrupo_from_dict(dic)
    elif tipo == TipoPedido.DESCONECTAR:
        return PedidoDesconectar.PedidoDesconectar_from_dict(dic)
    else:
        return None


def codificar(obj):
    if isinstance(obj, JSONserializable):
        return obj.to_json().encode()

    elif isinstance(obj, dict):
        for chave, valor in obj.items():
            if isinstance(valor, JSONserializable):
                obj[chave] = valor.to_json()
        return dumps(obj).encode()

    elif isinstance(obj, list):
        for indice, item in enumerate(obj):
            if isinstance(item, JSONserializable):
                obj[indice] = item.to_json()
        return dumps(obj).encode()

    elif isinstance(obj, str):
        return obj.encode()

    else:
        return dumps(obj).encode()


def descodificar(obj):
    if obj:
        if isinstance(obj, bytes):
            obj = obj.decode()
        return loads(obj)
    else:
        return None


# TODO delete debug function
def debug_obj_check(obj):
    print(obj, type(obj))

