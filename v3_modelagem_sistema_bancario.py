from abc import ABC, abstractmethod
from datetime import datetime

# FIXME: CLASSES COMUNS #
class Conta:

    def __init__(self, numero, cliente):    
        self._saldo = 0.0
        self._numero = numero
        self._cliente = cliente
        self._agencia = "0001"
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero): # representação da instância no classmethod é com 'cls'
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        saldo_insuficiente = valor > saldo

        if saldo_insuficiente:
            print("\n X X X Não foi possível realizar a operação! Você não possui saldo suficiente. X X X ")
        elif valor > 0:
            self._saldo -= valor
            print("\o/ Saque realizado com sucesso!")
            return True
        else:
            print("\n X X X Operação falhou! O valor informado é inválido.  X X X ")
        
        return False
    
    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            print("\o/ Depósito realizado com sucesso!")
        else:
            print("\n X X X Operação falhou! O valor informado é inválido.  X X X ")
            return False
        
        return True

class ContaCorrente(Conta):

    def __init__(self, numero, cliente, valor_max_saque=500, limite_saques=3):

        super().__init__(numero, cliente)
        self.valor_max_saque = valor_max_saque
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_valor_max = valor > self.valor_max_saque
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_valor_max:
            print("\n X X X Operação falhou! O valor do saque excede o limite. X X X ")

        elif excedeu_saques:
            print("\n X X X Operação falhou! Número máximo de saques excedido. X X X ")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico(Conta):
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Cliente(Conta):
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf


# FIXME: Classes abstratas e interfaces#
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

saldo = Conta(1, "João")
print(saldo.saldo)
print(saldo.historico)