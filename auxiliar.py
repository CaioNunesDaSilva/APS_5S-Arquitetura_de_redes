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
        json = dumps(obj)
        return json.encode()

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: auxiliar\nFuncao: codificar")
        print(erro)


def descodificar(obj):
    try:
        json = obj.decode()
        return loads(json)

    # TODO too broad exception clause
    except Exception as erro:
        print("Modulo: auxiliar\nFuncao: descodificar")
        print(erro)