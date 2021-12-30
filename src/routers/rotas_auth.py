from logging import log
from os import access
from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST
from src.schemas.schemas import LoginSucesso, Usuario, UsuarioSimples, LoginData
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorio.repositorio_usuario \
    import RepositorioUsuario
from src.infra.providers import hash_provider, token_provider
from src.routers.auth_utils import obter_usuario_logado

router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSimples)
def singup(usuario: Usuario, session: Session = Depends(get_db)):
    # Verificar se já existe tal usuário
    usuario_localizado = RepositorioUsuario(session).obter_por_telefone(usuario.telefone)
    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = f'Já existe um usuário para o telefone {usuario.telefone}')
    # Criar Usuário
    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(session).criar(usuario)
    return usuario_criado

@router.post('/token', response_model=LoginSucesso)
def login(login_data: LoginData, session: Session = Depends(get_db)):
    # Atributos do login
    telefone = login_data.telefone
    senha = login_data.senha
    
    # Verificação dos dados do login
        # Telefone
    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Telefone não constante')
        # Senha
    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)
    if not senha_valida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Senha está incorreta')
        
    # Gerar Token JWT
    token = token_provider.criar_access_token({'sub': usuario.telefone})
    return LoginSucesso(usuario=usuario, access_token=token)
    
@router.get('/me', response_model=UsuarioSimples)
def me(usuario: Usuario = Depends(obter_usuario_logado), session: Session = Depends(get_db)):
    return usuario
    
    
@router.get('/usuarios', status_code=status.HTTP_200_OK, response_model=List[UsuarioSimples])
def listar_usuarios(session: Session = Depends(get_db)):
    usuarios =  RepositorioUsuario(session).listar()
    return usuarios

@router.get('/usuarios/produtos', status_code=status.HTTP_200_OK, response_model=List[Usuario])
def listar_usuarios_com_produtos(session: Session = Depends(get_db)):
    usuarios =  RepositorioUsuario(session).listar()
    return usuarios