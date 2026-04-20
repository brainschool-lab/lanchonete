from dataclasses import dataclass
@dataclass
class Produto:
    codigo: int
    valor: float
    tipo: int
    desconto_percentual: float = 0.0

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("Valor do produto não pode ser negativo")
        if self.desconto_percentual < 0:
            raise ValueError("Desconto não pode ser negativo")

    def preco_final(self) -> float:
        #Regra: se tipo == 2 NÃO aplica desconto
        if self.tipo == 2:
            return float(self.valor)
        if self.desconto_percentual and self.desconto_percentual > 0:
            return float(self.valor) * (1 - self.desconto_percentual / 100)
        return float(self.valor)