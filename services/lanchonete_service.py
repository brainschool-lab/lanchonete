from domain.cliente import Cliente
from domain.pedido import Pedido
from domain.produto import Produto
from repositories.memory import db

class LanchoneteService:

    def criar_cliente(self, cpf: str, nome: str = "") -> Cliente:
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
        db.produtos_por_id[codigo] = produto
        return produto

    def obter_produto(self, codigo: int) -> Produto | None:
        return db.produtos_por_id.get(codigo)

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

    def cancelar_pedido(self, cod_pedido: int) -> bool:
        pedido = db.pedidos_por_codigo.get(cod_pedido)
        if pedido is None:
            return False
        return pedido.cancelar()

    def listar_pedidos_cancelados(self) -> list:
        return [p for p in db.pedidos_por_codigo.values() if p.esta_cancelado]

    def adicionar_observacao(self, cod_pedido: int, observacao: str) -> bool:
        pedido = db.pedidos_por_codigo.get(cod_pedido)
        if pedido is None:
            return False
        return pedido.adicionar_observacao(observacao)

    def buscar_observacao_pedido(self, cod_pedido: int):
        return db.pedidos_por_codigo.get(cod_pedido)

    def tornar_pedido_prioritario(self, cod_pedido: int) -> bool:
        pedido = db.pedidos_por_codigo.get(cod_pedido)
        if pedido is None:
            return False
        return pedido.tornar_prioritario()

    def listar_fila_preparo(self) -> list:
        pedidos_ativos = [
            p for p in db.pedidos_por_codigo.values()
            if not p.esta_cancelado and not p.esta_entregue
        ]
        pedidos_ativos.sort(key=lambda p: not p.prioritario)
        return pedidos_ativos

service = LanchoneteService()