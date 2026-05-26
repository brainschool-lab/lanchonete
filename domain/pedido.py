from typing import List
from domain.cliente import Cliente
from domain.produto import Produto

class Pedido:
    _seq = 1

    def __init__(self, cliente: Cliente, qtd_max_produtos: int):
        if int(qtd_max_produtos) <= 0:
            raise ValueError("Quantidade máxima deve ser maior que zero")

        self._codigo = Pedido._seq
        Pedido._seq += 1
        self.cliente = cliente
        self.qtd_max_produtos = int(qtd_max_produtos)
        self.listaProdutos: List[Produto] = []
        self.esta_entregue: bool = False
        self.esta_cancelado: bool = False
        self.prioritario: bool = False
        self.observacao: str = ""

    @property
    def codigo(self) -> int:
        return self._codigo

    def adicionar_produto(self, produto: Produto) -> bool:
        if len(self.listaProdutos) >= self.qtd_max_produtos:
            return False
        self.listaProdutos.append(produto)
        return True

    def finalizar(self) -> float:
        self.esta_entregue = True
        total = 0.0
        for p in self.listaProdutos:
            total += p.preco_final()
        return float(total)

    def total_se_finalizado(self) -> float:
        if not self.esta_entregue:
            return 0.0
        total = 0.0
        for p in self.listaProdutos:
            total += p.preco_final()
        return float(total)

    def adicionar_observacao(self, observacao: str) -> bool:
        if self.esta_entregue:
            return False
        if observacao is None:
            return False

        observacao = observacao.strip()
        if observacao == "":
            return False
        if len(observacao) > 200:
            return False

        self.observacao = observacao
        return True

    def cancelar(self) -> bool:
        if self.esta_entregue or self.esta_cancelado:
            return False
        self.esta_cancelado = True
        return True

    def tornar_prioritario(self) -> bool:
        if self.esta_entregue or self.esta_cancelado:
            return False
        self.prioritario = True
        return True