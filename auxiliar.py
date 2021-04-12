from enum import Enum


class DadosCliente:
    def __init__(self, nome: str, senha: str, soquete):
        try:
            self._nome = nome
            self._senha = senha
            self._soquete = soquete

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: DadosCliente\nMetodo: __init__")
            print(erro)

    @property
    def nome(self):
        try:
            return self._nome

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: DadosCliente\nMetodo: nome")
            print(erro)

    @property
    def senha(self):
        try:
            return self._senha

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: DadosCliente\nMetodo: senha")
            print(erro)

    @property
    def soquete(self):
        try:
            return self._soquete

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: DadosCliente\nMetodo: soquete")
            print(erro)


class TipoMenssagem(Enum):
    CADASTRO = 0
    LOGIN = 1
    MENSSAGEM_PRIVADA = 2
    MENSSAGEM_GRUPO = 3
    DESCONECTAR = 4

    @staticmethod
    def converte_tipo_valor(tipo):
        return tipo.value

    @staticmethod
    def converte_valor_tipo(valor):
        for tipo in TipoMenssagem:
            if valor == tipo.value:
                return tipo

