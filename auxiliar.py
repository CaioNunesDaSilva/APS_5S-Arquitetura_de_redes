class Entidade:
    def __init__(self, codigo: int, nome: str):
        self._codigo = codigo
        self._nome = nome

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


class Usuario(Entidade):
    def __init__(self, codigo: int, nome: str, conexao, endereco):
        super().__init__(codigo, nome)
        self._conexao = conexao
        self._endereco = endereco

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


class Grupo(Entidade):
    def __init__(self, codigo: int, nome: str, dono: Usuario, membros: list):
        super().__init__(codigo, nome)
        self._dono = dono
        self._membros = membros

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


class Pedido:
    def __init__(self, nome: str, senha: str):
        self._nome = nome
        self._senha = senha

    @property
    def nome(self):
        try:
            return self._nome
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def senha(self):
        try:
            return self._senha
        # TODO too broad exception clause
        except Exception:
            raise


class PedidoCadastro(Pedido):
    pass


class PedidoLogin(Pedido):
    pass


class Mensagem:
    def __init__(self, mensagem: str, remetente: Usuario):
        self._mensagem = mensagem
        self._remetente = remetente

    @property
    def mensagem(self):
        try:
            return self._mensagem
        # TODO too broad exception clause
        except Exception:
            raise

    @property
    def remetente(self):
        try:
            return self._remetente
        # TODO too broad exception clause
        except Exception:
            raise


class MensagemPrivado(Mensagem):
    def __init__(self, mensagem: str, remetente: Usuario, destinatario: Usuario):
        super().__init__(mensagem, remetente)
        self._destinatario = destinatario

    @property
    def destinatario(self):
        try:
            return self._destinatario
        # TODO too broad exception clause
        except Exception:
            raise


class MensagemGrupo(Mensagem):
    def __init__(self, mensagem: str, remetente: Usuario, grupo: Grupo):
        super().__init__(mensagem, remetente)
        self._grupo = grupo

    @property
    def grupo(self):
        try:
            return self._grupo
        # TODO too broad exception clause
        except Exception:
            raise
