from fastapi import FastAPI, Depends, status
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Produto, ProdutoSimples
from src.infra.sqlalchemy.config.database import get_db, create_db
from src.infra.sqlalchemy.repositorio.produto import RepositorioProduto

create_db()

app = FastAPI()


@app.get('/produtos', status_code=status.HTTP_200_OK, response_model=List[ProdutoSimples])
def listar_produtos(db: Session = Depends(get_db)):
    produtos =  RepositorioProduto(db).listar()
    return produtos


@app.post('/produtos', status_code=status.HTTP_201_CREATED, response_model=ProdutoSimples)
def criar_produto(produto: Produto, db: Session = Depends(get_db)):
    produto_criado = RepositorioProduto(db).criar(produto)
    return produto_criado