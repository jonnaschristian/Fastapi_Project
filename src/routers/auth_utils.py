from fastapi import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Session
from starlette import status
from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import token_provider
from jose import JWTError

from src.infra.sqlalchemy.repositorio.repositorio_usuario import RepositorioUsuario

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')


def obter_usuario_logado(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    # Decodificar o Token, pegar o telefone, buscar usuario no db e retornar
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token inválido')
    try:
        telefone = token_provider.verificar_access_token(token)
    except JWTError:
        raise exception
    if not telefone:
        raise exception
        
    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)
    if not usuario:
        raise exception
    
    return usuario