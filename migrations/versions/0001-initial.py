from alembic import op
import sqlalchemy as sa

revision = 'f267817ee444'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('senha_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('categoria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('criado_por_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['criado_por_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('anuncio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=200), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.Column('preco', sa.Float(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('categoria_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('compra',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('valor_pago', sa.Float(), nullable=False),
    sa.Column('data_compra', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('anuncio_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['anuncio_id'], ['anuncio.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorito',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('anuncio_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['anuncio_id'], ['anuncio.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pergunta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('texto', sa.Text(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('anuncio_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['anuncio_id'], ['anuncio.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resposta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('texto', sa.Text(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=True),
    sa.Column('pergunta_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pergunta_id'], ['pergunta.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('resposta')
    op.drop_table('pergunta')
    op.drop_table('favorito')
    op.drop_table('compra')
    op.drop_table('anuncio')
    op.drop_table('categoria')
    op.drop_table('usuario')
