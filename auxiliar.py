
class Usuario:
    def __init__(self, codigo: int, nome: str, conexao, endereco):
        self._codigo = codigo
        self._nome = nome
        self._conexao = conexao
        self._endereco = endereco

    @property
    def codigo(self):
        try:
            return self._codigo
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def nome(self):
        try:
            return str(self._nome)
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def conexao(self):
        try:
            return self._conexao
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def endereco(self):
        try:
            return self._endereco
        # TODO too broad exception clause
        except Exception:
            raise


class Grupo:
    def __init__(self, codigo: int, nome: str, dono: Usuario, membros: list):
        self._codigo = codigo
        self._nome = nome
        self._dono = dono
        self._membros = membros

    @property
    def codigo(self):
        try:
            return self._codigo
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def nome(self):
        try:
            return self._nome
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def dono(self):
        try:
            return self._dono
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def membros(self):
        try:
            return self._membros
        # TODO too broad exception clause
        except Exception:
            raise
