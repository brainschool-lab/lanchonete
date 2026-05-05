from fastapi import APIRouter, HTTPException
from schemas.pedido import (
        PedidoCreate, 
        PedidoAddItem, 
        PedidoOut,
        PedidoCanceled
    )
from services.lanchonete_service import service

router = APIRouter(prefix="/lanchonete/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoOut)
def criar(payload: PedidoCreate):
    """Cria um pedido com o primeiro produto já adicionado."""
    pedido = service.criar_pedido(payload.cpf, payload.cod_produto, payload.qtd_max_produtos)
    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Cliente ou produto não encontrado"
        )

    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )


@router.put("/{cod_pedido}/itens")
def adicionar_item(cod_pedido: int, payload: PedidoAddItem):
    """Adiciona um produto a um pedido existente."""
    ok = service.alterar_pedido(cod_pedido, payload.cod_produto)
    if not ok:
        raise HTTPException(
            status_code=400,
            detail="Pedido/produto inválido ou limite excedido"
        )
    return {"ok": True}


@router.post("/{cod_pedido}/finalizar")
def finalizar(cod_pedido: int):
    """Finaliza um pedido e retorna o total calculado."""
    total = service.finalizar_pedido(cod_pedido)
    if total is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"total": total}


@router.get("/{cod_pedido}", response_model=PedidoOut)
def obter(cod_pedido: int):
    """Busca um pedido pelo código."""
    pedido = service.obter_pedido(cod_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )

#TODO: Incluir Cancela pedido (Retorno:´400´)    
@router.delete("/{cod_pedido}", response_model=PedidoCanceled)
def delete_product(cod_pedido: int):
    delete = service.delete_product(cod_pedido)
    if not delete:
        raise HTTPException (
            status_code=400,
            detail="Pedido inválido."   
        )

    return {
        "status": "OK",
        "mensagem": "Pedido cancelado com sucesso!"
    }
    
#TODO: Lista pedidos cancelados. (Retorno: 404)

@router.get("/{cod_pedido}", response_model=PedidoCanceled)
def pedido_canceled(cod_pedido: int):
    pedido = service.obter_pedido(cod_pedido)
    if not pedido:
        raise HTTPException (
            status_code=404,
            detail="Os pedidos não foram encontrados."
        )
    return PedidoOut(
        codigo=pedido.codigo,
        cpf=pedido.cliente.cpf,
        esta_entregue=pedido.esta_entregue,
        produtos=[p.codigo for p in pedido.listaProdutos],
    )