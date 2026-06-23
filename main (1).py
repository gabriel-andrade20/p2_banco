from fastapi import FastAPI
from app.routes import pedidos

app = FastAPI(title="API de Pedidos")

app.include_router(pedidos.router, prefix="/pedidos", tags=["pedidos"])
