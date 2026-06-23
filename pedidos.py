from fastapi import APIRouter, HTTPException
from app.models import PedidoEntrada, Pedido
from app.database import colecao_pedidos
from app.mensageria import publicar_rabbitmq, publicar_kafka
import uuid

router = APIRouter()


@router.post("/", response_model=Pedido, status_code=201)
def criar_pedido(dados: PedidoEntrada):
    pedido = {
        "id": str(uuid.uuid4()),
        "nome_cliente": dados.nome_cliente,
        "nome_produto": dados.nome_produto,
        "quantidade": dados.quantidade,
        "status": "PENDENTE",
    }

    colecao_pedidos.insert_one({**pedido})

    try:
        publicar_rabbitmq({"id": pedido["id"], "status": pedido["status"]})
    except Exception:
        pass

    try:
        publicar_kafka(pedido)
    except Exception:
        pass

    return pedido


@router.get("/", response_model=list[Pedido])
def listar_pedidos():
    pedidos = list(colecao_pedidos.find({}, {"_id": 0}))
    return pedidos
