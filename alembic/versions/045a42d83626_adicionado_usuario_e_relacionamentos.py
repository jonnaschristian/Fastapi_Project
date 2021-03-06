"""Adicionado Usuario e Relacionamentos

Revision ID: 045a42d83626
Revises: 
Create Date: 2021-12-27 13:39:50.590356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '045a42d83626'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('senha', sa.String(), nullable=True),
    sa.Column('telefone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_usuario_id'), ['id'], unique=False)

    op.create_table('produto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('detalhes', sa.String(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.Column('disponivel', sa.Boolean(), nullable=True),
    sa.Column('tamanhos', sa.String(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name='fk_usuario'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_produto_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_produto_id'))

    op.drop_table('produto')
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_usuario_id'))

    op.drop_table('usuario')
    # ### end Alembic commands ###
