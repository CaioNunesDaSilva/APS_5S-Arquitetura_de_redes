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


class Entidade:
    def __init__(self, codigo: int, nome: str):
        try:
            self._codigo = codigo
            self._nome = nome

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Entidade\nMetodo: __init__")
            print(erro)

    @property
    def codigo(self):
        try:
            return self._codigo

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Entidade\nMetodo: codigo")
            print(erro)

    @property
    def nome(self):
        try:
            return str(self._nome)

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Entidade\nMetodo: nome")
            print(erro)


class Usuario(Entidade):
    def __init__(self, codigo: int, nome: str, conexao, endereco):
        try:
            super().__init__(codigo, nome)
            self._conexao = conexao
            self._endereco = endereco

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Usuario\nMetodo: __init__")
            print(erro)

    @property
    def conexao(self):
        try:
            return self._conexao

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Usuario\nMetodo: conexao")
            print(erro)

    @property
    def endereco(self):
        try:
            return self._endereco

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Usuario\nMetodo: endereco")
            print(erro)


class Grupo(Entidade):
    def __init__(self, codigo: int, nome: str, dono: Usuario, membros: list):
        try:
            super().__init__(codigo, nome)
            self._dono = dono
            self._membros = membros

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Grupo\nMetodo: __init__")
            print(erro)

    @property
    def dono(self):
        try:
            return self._dono

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Grupo\nMetodo: dono")
            print(erro)

    @property
    def membros(self):
        try:
            return self._membros

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Grupo\nMetodo: membros")
            print(erro)


class Pedido:
    def __init__(self, nome: str, senha: str):
        try:
            self._nome = nome
            self._senha = senha

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Pedido\nMetodo: __init__")
            print(erro)

    @property
    def nome(self):
        try:
            return self._nome

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Pedido\nMetodo: nome")
            print(erro)

    @property
    def senha(self):
        try:
            return self._senha

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Pedido\nMetodo: senha")
            print(erro)


class PedidoCadastro(Pedido):
    pass


class PedidoLogin(Pedido):
    pass


class Mensagem:
    def __init__(self, mensagem: str, remetente: Usuario):
        try:
            self._mensagem = mensagem
            self._remetente = remetente

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Mensagem\nMetodo: __init__")
            print(erro)

    @property
    def mensagem(self):
        try:
            return self._mensagem

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Mensagem\nMetodo: mensagem")
            print(erro)

    @property
    def remetente(self):
        try:
            return self._remetente

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: Mensagem\nMetodo: remetente")
            print(erro)


class MensagemPrivado(Mensagem):
    def __init__(self, mensagem: str, remetente: Usuario, destinatario: Usuario):
        try:
            super().__init__(mensagem, remetente)
            self._destinatario = destinatario

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: MensagemPrivado\nMetodo: __init__")
            print(erro)

    @property
    def destinatario(self):
        try:
            return self._destinatario

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: MensagemPrivado\nMetodo: destinatario")
            print(erro)


class MensagemGrupo(Mensagem):
    def __init__(self, mensagem: str, remetente: Usuario, grupo: Grupo):
        try:
            super().__init__(mensagem, remetente)
            self._grupo = grupo

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: MensagemGrupo\nMetodo: __init__")
            print(erro)

    @property
    def grupo(self):
        try:
            return self._grupo

        # TODO too broad exception clause
        except Exception as erro:
            print("Modulo: auxiliar\nClasse: MensagemGrupo\nMetodo: grupo")
            print(erro)
