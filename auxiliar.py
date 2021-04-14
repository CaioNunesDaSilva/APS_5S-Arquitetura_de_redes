from enum import Enum
from json import dumps
from json import loads


class JSONserializable:
    def to_json(self):
        try:
            return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: JSONserializable\nMetodo: to_json")
            print(erro)


class ObjetoDB:
    def __init__(self, codigo: int, nome: str, ):
        try:
            self.codigo = codigo
            self.nome = nome

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: ObjetoDB\nMetodo: __init__")
            print(erro)


class Usuario(ObjetoDB, JSONserializable):
    def __init__(self, codigo: int, nome: str, senha: str):
        try:
            self.senha = senha
            super().__init__(codigo, nome)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Usuario\nMetodo: __init__")
            print(erro)

    def __eq__(self, other):
        try:
            return self.nome == other.nome

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Usuario\nMetodo: __eq__")
            print(erro)

    @staticmethod
    def usuario_from_dict(dic):
        try:
            return Usuario(dic["codigo"], dic["nome"], dic["senha"])

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Usuario\nMetodo: usuario_from_dict")
            print(erro)


class Grupo(ObjetoDB, JSONserializable):
    def __init__(self, codigo: int, nome: str, membros: [Usuario], dono: Usuario):
        try:
            self.membros = membros
            self.dono = dono
            super().__init__(codigo, nome)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Grupo\nMetodo: __init__")
            print(erro)

    @staticmethod
    def grupo_from_dict(dic):
        try:
            return Grupo(dic["codigo"], dic["nome"], dic["membros"], dic["dono"])

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Grupo\nMetodo: grupo_from_dict")
            print(erro)


class TipoMenssagem(Enum):
    CADASTRO_USUARIO = 0
    LOGIN = 1
    ATUALIZAR_LISTA_CLIENTES = 2
    ATUALIZAR_LISTA_GRUPOS = 3
    MENSSAGEM_PRIVADA = 4
    MENSSAGEM_GRUPO = 5
    CADASTRO_GRUPO = 6
    DESCONECTAR = 7

    @staticmethod
    def converter_valor_tipo(valor):
        try:
            for tipo in TipoMenssagem:
                if valor == tipo.value:
                    return tipo

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: TipoMenssagem\nMetodo: converter_valor_tipo")
            print(erro)


def codificar(obj):
    try:
        if isinstance(obj, dict):
            for chave, valor in obj.items():
                if isinstance(valor, Usuario) or isinstance(valor, Grupo):
                    obj[chave] = valor.to_json()
            obj = dumps(obj)
            return obj.encode()

        elif isinstance(obj, list):
            for posicao, valor in enumerate(obj):
                if isinstance(valor, Usuario) or isinstance(valor, Grupo):
                    obj[posicao] = valor.to_json()
            obj = dumps(obj)
            return obj.encode()

        elif isinstance(obj, Usuario) or isinstance(obj, Grupo):
            return obj.to_json().encode()

        else:
            obj = dumps(str(obj))
            return obj.encode()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: auxiliar\nFuncao: codificar")
        print(erro)


def descodificar(obj):
    try:
        if isinstance(obj, bytes):
            obj = obj.decode()
        return loads(obj)

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: auxiliar\nFuncao: descodificar")
        print(erro)


# TODO delete debug function
def debug_obj_check(obj):
    print(obj, type(obj))
