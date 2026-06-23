from pydantic import BaseModel, Field
from enum import Enum


class StatusPedido(str, Enum):
    PENDENTE = "PENDENTE"


class PedidoEntrada(BaseModel):
    nome_cliente: str
    nome_produto: str
    quantidade: int


class Pedido(BaseModel):
    id: str
    nome_cliente: str
    nome_produto: str
    quantidade: int
    status: str = StatusPedido.PENDENTE
