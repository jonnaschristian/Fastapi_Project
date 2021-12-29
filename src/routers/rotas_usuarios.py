from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Usuario
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorio.repositorio_usuario \
    import RepositorioUsuario


router = APIRouter()



@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=Usuario)
def singup(usuario: Usuario, session: Session = Depends(get_db)):
    usuario_criado = RepositorioUsuario(session).criar(usuario)
    return usuario_criado

@router.get('/usuarios', status_code=status.HTTP_200_OK, response_model=List[Usuario])
def listar_usuarios(session: Session = Depends(get_db)):
    usuarios =  RepositorioUsuario(session).listar()
    return usuarios