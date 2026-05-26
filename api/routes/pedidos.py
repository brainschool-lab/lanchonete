from fastapi import APIRouter, HTTPException
from schemas.pedido import PedidoCreate, PedidoAddItem, PedidoOut, ObservacaoInput, ObservacaoOut, PedidoFilaOut
from services.lanchonete_service import service

router = APIRouter(prefix="/lanchonete/pedidos", tags=["pedidos"])

@router.post("", response_model=PedidoOut)
def criar(payload: PedidoCreate):
    pedido = service.criar_pedido(payload.cpf, payload.cod_produto, payload.qtd_max_produtos)
    if not pedido:
        raise HTTPException(status_code=404, detail="Cliente ou produto não encontrado")
    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        esta_cancelado=pedido.esta_cancelado,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )

@router.put("/{cod_pedido}/itens")
def adicionar_item(cod_pedido: int, payload: PedidoAddItem):
    ok = service.alterar_pedido(cod_pedido, payload.cod_produto)
    if not ok:
        raise HTTPException(status_code=400, detail="Pedido/produto inválido ou limite excedido")
    return {"ok": True}

@router.post("/{cod_pedido}/finalizar")
def finalizar(cod_pedido: int):
    total = service.finalizar_pedido(cod_pedido)
    if total is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"total": total}

@router.get("/cancelados", response_model=list[PedidoOut])
def listar_pedidos_cancelados():
    pedidos = service.listar_pedidos_cancelados()
    return [
        PedidoOut(
            codigo=p.codigo,
            cpf=p.cliente.cpf,
            esta_entregue=p.esta_entregue,
            esta_cancelado=p.esta_cancelado,
            produtos=[prod.codigo for prod in p.listaProdutos],
        )
        for p in pedidos
    ]

@router.get("/fila/preparo", response_model=list[PedidoFilaOut])
def listar_fila_preparo():
    pedidos = service.listar_fila_preparo()
    return [
        PedidoFilaOut(
            codigo=p.codigo,
            cpf=p.cliente.cpf,
            prioritario=p.prioritario,
            observacao=p.observacao,
        )
        for p in pedidos
    ]

@router.get("/{cod_pedido}", response_model=PedidoOut)
def obter(cod_pedido: int):
    pedido = service.obter_pedido(cod_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        esta_cancelado=pedido.esta_cancelado,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )

@router.post("/{cod_pedido}/cancelar")
@router.patch("/{cod_pedido}/cancelar")
def cancelar_pedido(cod_pedido: int):
    resultado = service.cancelar_pedido(cod_pedido)
    if not resultado:
        raise HTTPException(status_code=400, detail="Pedido não encontrado ou não pode ser cancelado")
    return {"ok": True, "mensagem": "Pedido cancelado com sucesso"}

@router.post("/{cod_pedido}/prioridade")
def tornar_pedido_prioritario(cod_pedido: int):
    resultado = service.tornar_pedido_prioritario(cod_pedido)
    if not resultado:
        raise HTTPException(status_code=400, detail="Pedido não encontrado ou não pode se tornar prioritário")
    return {"ok": True, "mensagem": "Pedido definido como prioritário"}

@router.post("/{cod_pedido}/observacao")
def adicionar_observacao(cod_pedido: int, body: ObservacaoInput):
    resultado = service.adicionar_observacao(cod_pedido, body.observacao)
    if not resultado:
        raise HTTPException(status_code=400, detail="Pedido não encontrado ou inválido")
    return {"ok": True, "mensagem": "Observação adicionada com sucesso"}

@router.get("/{cod_pedido}/observacao", response_model=ObservacaoOut)
def buscar_observacao(cod_pedido: int):
    pedido = service.buscar_observacao_pedido(cod_pedido)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return ObservacaoOut(
        codigo=pedido.codigo,
        observacao=pedido.observacao,
    )