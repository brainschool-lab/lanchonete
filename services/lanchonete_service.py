from domain.cliente import Cliente
from domain.pedido import Pedido
from domain.produto import Produto
from repositories.memory import db

class LanchoneteService:
    def criar_cliente(self, cpf: str, nome: str = "") -> Cliente:
        #regra simples: se já existe, retorna o mesmo
        if not cpf.strip():
            raise ValueError("CPF não pode ser vazio")

        if cpf in db.clientes_por_cpf:
            return db.clientes_por_cpf[cpf]
        cliente = Cliente(cpf=cpf, nome=nome)
        db.clientes_por_cpf[cpf] = cliente
        return cliente

    def obter_cliente(self, cpf: str) -> Cliente | None:
        return db.clientes_por_cpf.get(cpf)

    def criar_produto(self, codigo: int, valor: float, tipo: int, desconto_percentual: float = 0.0) -> Produto:
        produto = Produto(codigo=codigo, valor=valor, tipo=tipo, desconto_percentual=desconto_percentual)
        db.produtos_por_codigo[codigo] = produto
        return produto

    def obter_produto(self, codigo: int) -> Produto | None:
        return db.produtos_por_codigo.get(codigo)

    def alterar_valor_produto(self, codigo: int, novo_valor: float) -> bool:
        produto = self.obter_produto(codigo)
        if not produto:
            return False
        produto.valor = novo_valor
        return True

    def criar_pedido(self, cpf: str, cod_produto: int, qtd_max_produtos: int) -> Pedido | None:
        cliente = self.obter_cliente(cpf)
        produto = self.obter_produto(cod_produto)
        if not cliente or not produto:
            return None
        pedido = Pedido(cliente=cliente, qtd_max_produtos=qtd_max_produtos)
        if not pedido.adicionar_produto(produto):
            return None
        db.pedidos_por_codigo[pedido.codigo] = pedido
        return pedido
    
    def alterar_pedido(self, cod_pedido: int, cod_produto: int) -> bool:
        pedido = db.pedidos_por_codigo.get(cod_pedido)
        produto = self.obter_produto(cod_produto)
        if not pedido or not produto:
            return False
        return pedido.adicionar_produto(produto)
    
    def finalizar_pedido(self, cod_pedido: int) -> float | None:
        pedido = db.pedidos_por_codigo.get(cod_pedido)
        if not pedido:
            return None
        return pedido.finalizar()
    
    def obter_pedido(self, cod_pedido: int) -> Pedido | None:
        return db.pedidos_por_codigo.get(cod_pedido)

service = LanchoneteService()