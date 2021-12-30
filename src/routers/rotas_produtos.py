from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Produto, ProdutoSimples
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorio.repositorio_produto import RepositorioProduto


router = APIRouter()


@router.get('/produtos', status_code=status.HTTP_200_OK, response_model=List[Produto])
def listar_produtos(session: Session = Depends(get_db)):
    produtos =  RepositorioProduto(session).listar()
    return produtos

@router.get('/produtos/{id}')
def exibir_produto(id: int, session: Session = Depends(get_db)):
    produto_localizado = RepositorioProduto(session).buscarPorId(id)
    if not produto_localizado:
        raise HTTPException(status_code=404, detail=f'Não há produto com o ID = {id}')
    return produto_localizado

@router.post('/produtos', status_code=status.HTTP_201_CREATED, response_model=Produto)
def criar_produto(produto: Produto, session: Session = Depends(get_db)):
    produto_criado = RepositorioProduto(session).criar(produto)
    return produto_criado

@router.put('/produtos/{id}', status_code=status.HTTP_200_OK, response_model=ProdutoSimples)
def atualizar_produto(id: int, produto: Produto, session: Session = Depends(get_db)):
    RepositorioProduto(session).editar(id, produto)
    produto.id = id
    return produto

@router.delete('/produtos/{id}', status_code=status.HTTP_200_OK)
def remover_produto(id: int, session: Session = Depends(get_db)):
    consulta = RepositorioProduto(session).remover(id)
    if not consulta:
        raise HTTPException(status_code=404, detail=f'Não há produto com o ID = {id}')
    return {"msg": "Produto Removido"}