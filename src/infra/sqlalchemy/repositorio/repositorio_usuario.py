from sqlalchemy import select
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models


class RepositorioUsuario():
    def __init__(self, session: Session):
        self.session = session

    def criar(self, usuario: schemas.Usuario):
        usuario_db = models.Usuario(
            nome = usuario.nome,
            senha = usuario.senha,
            telefone = usuario.telefone
        )
        self.session.add(usuario_db)
        self.session.commit()
        self.session.refresh(usuario_db)
        return usuario_db
        
    def listar(self):
        stmt = select(models.Usuario)
        usuarios = self.session.execute(stmt).scalars().all()
        return usuarios
    
    def obter_por_telefone(self, telefone) -> models.Usuario:
        consulta = select(models.Usuario).where(
            models.Usuario.telefone == telefone)
        return self.session.execute(consulta).scalars().first()

    def remover(self):
        pass
