# Pedidos API

API para gerenciamento de pedidos de um e-commerce, feita com FastAPI, MongoDB, RabbitMQ e Kafka.

## Como rodar

Precisa ter o Docker instalado. Com ele, um único comando sobe tudo:

```bash
docker compose up --build
```

A API vai estar disponível em `http://localhost:8000`
A documentação interativa fica em `http://localhost:8000/docs`

## Endpoints

**Criar um pedido**
```
POST /pedidos/
```
```json
{
  "nome_cliente": "João Silva",
  "nome_produto": "Teclado Mecânico",
  "quantidade": 1
}
```

**Listar todos os pedidos**
```
GET /pedidos/
```

## Testes

```bash
pip install -r requirements.txt
pytest tests/
```

## Tecnologias

- FastAPI
- MongoDB
- RabbitMQ
- Kafka
- Docker
