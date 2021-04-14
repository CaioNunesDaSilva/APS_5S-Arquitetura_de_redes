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
    def __init__(self, codigo: int, nome: str, senha: str):
        self.senha = senha
        super().__init__(codigo, nome)

    def to_json(self):
        self.codigo = str(self.codigo)
        return super().to_json()

    def __eq__(self, other):
        return self.nome == other.nome

    @staticmethod
    def Usuario_from_dict(dic):
        return Usuario(int(dic["codigo"]), dic["nome"], dic["senha"])


class Grupo(ObjetoDB, JSONserializable):
    def __init__(self, codigo: int, nome: str, membros: [Usuario], dono: Usuario):
        self.membros = membros
        self.dono = dono
        super().__init__(codigo, nome)

    def __eq__(self, other):
        return self.nome == other.nome

    @staticmethod
    def Grupo_from_dict(dic):
        return Grupo(dic["codigo"], dic["nome"], dic["membros"], dic["dono"])


class Pedido(JSONserializable):
    def __init__(self, tipo: TipoPedido):
        self.tipo = tipo

    def to_json(self):
        self.tipo = self.tipo.to_json()
        return super().to_json()


class PedidoCadastroUsuario(Pedido):
    def __init__(self, tipo: TipoPedido, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
        super().__init__(tipo)

    @staticmethod
    def PedidoCadastroUsuario_from_dict(dic):
        return PedidoCadastroUsuario(TipoPedido.from_str(dic["tipo"]), dic["nome"], dic["senha"])


class PedidoLogin(Pedido):
    def __init__(self, tipo: TipoPedido, nome: str, senha: str):
        self.nome = nome
        self.senha = senha
        super().__init__(tipo)

    @staticmethod
    def PedidoLogin_from_dict(dic):
        return PedidoLogin(TipoPedido.from_str(dic["tipo"]), dic["nome"], dic["senha"])


class PedidoAtualizarListaClientes(Pedido):
    def __init__(self, tipo: TipoPedido, remetente: Usuario):
        self.remetente = remetente
        super().__init__(tipo)

    def to_json(self):
        self.remetente = self.remetente.to_json()
        return super().to_json()

    @staticmethod
    def PedidoAtualizarListaClientes_from_dict(dic):
        return PedidoAtualizarListaClientes(TipoPedido.from_str(dic["tipo"]),
                                            Usuario.Usuario_from_dict(descodificar(dic["remetente"])))


def codificar(obj):
    if isinstance(obj, str):
        return obj.encode()
    return dumps(obj).encode()


def descodificar(obj):
    if isinstance(obj, bytes):
        obj = obj.decode()
    return loads(obj)


# TODO delete debug function
def debug_obj_check(obj):
    print(obj, type(obj))
