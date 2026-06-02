"""initial_schema

Revision ID: 46226f422f07
Revises: 
Create Date: 2026-06-02 16:08:26.825917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46226f422f07'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. operadora
    op.create_table(
        'operadora',
        sa.Column('ID', sa.Integer(), nullable=False),
        sa.Column('NOME', sa.String(length=100), nullable=True),
        sa.Column('CONCESSIONARIA', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('ID')
    )

    # 2. veiculos
    op.create_table(
        'veiculos',
        sa.Column('NUM_VEIC', sa.Integer(), nullable=False),
        sa.Column('IDN_PLAC_VEIC', sa.String(length=10), nullable=True),
        sa.Column('VEIC_ATIV_EMPR', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.PrimaryKeyConstraint('NUM_VEIC'),
        sa.UniqueConstraint('IDN_PLAC_VEIC')
    )

    # 3. linha
    op.create_table(
        'linha',
        sa.Column('COD_LINH', sa.String(length=10), nullable=False),
        sa.Column('ID_OPERADORA', sa.Integer(), nullable=True),
        sa.Column('COMPARTILHADA', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('LINH_ATIV_EMPR', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.ForeignKeyConstraint(['ID_OPERADORA'], ['operadora.ID'], ),
        sa.PrimaryKeyConstraint('COD_LINH')
    )

    # 4. auto_infracao
    op.create_table(
        'auto_infracao',
        sa.Column('NUM_AI', sa.String(length=10), nullable=False),
        sa.Column('NUM_NOTF', sa.String(length=10), nullable=True),
        sa.Column('TIP_PENL', sa.String(length=20), nullable=True),
        sa.Column('NOM_CONC', sa.String(length=100), nullable=True),
        sa.Column('COD_LINH', sa.String(length=10), nullable=True),
        sa.Column('NOM_LINH', sa.String(length=100), nullable=True),
        sa.Column('NUM_VEIC', sa.Integer(), nullable=True),
        sa.Column('IDN_PLAC_VEIC', sa.String(length=10), nullable=True),
        sa.Column('DAT_OCOR_INFR', sa.DateTime(), nullable=True),
        sa.Column('DES_LOCA', sa.String(length=255), nullable=True),
        sa.Column('COD_IRRG_FISC', sa.Integer(), nullable=True),
        sa.Column('ARTIGO', sa.String(length=20), nullable=True),
        sa.Column('DES_OBSE', sa.String(length=255), nullable=True),
        sa.Column('NUM_MATR_FISC', sa.Integer(), nullable=True),
        sa.Column('QTE_PONT', sa.Integer(), nullable=True),
        sa.Column('DAT_EMIS_NOTF', sa.DateTime(), nullable=True),
        sa.Column('DAT_LIMT_RECU', sa.DateTime(), nullable=True),
        sa.Column('VAL_INFR', sa.Float(), nullable=True),
        sa.Column('DAT_CANC', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('NUM_AI'),
        sa.UniqueConstraint('NUM_NOTF')
    )

    # 5. recurso_primeira_instancia
    op.create_table(
        'recurso_primeira_instancia',
        sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('NUM_AI', sa.String(length=15), nullable=True),
        sa.Column('NUM_ATA', sa.Integer(), nullable=True),
        sa.Column('NUM_RECURSO', sa.String(length=15), nullable=True),
        sa.Column('NOM_CONC', sa.String(length=100), nullable=True),
        sa.Column('RESULTADO', sa.Boolean(), nullable=False),
        sa.Column('DAT_PUBL', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('ID'),
        sa.UniqueConstraint('NUM_AI')
    )

    # 6. recurso_segunda_instancia
    op.create_table(
        'recurso_segunda_instancia',
        sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('NUM_AI', sa.String(length=15), nullable=True),
        sa.Column('NUM_RECURSO', sa.String(length=15), nullable=True),
        sa.Column('NOM_CONC', sa.String(length=100), nullable=True),
        sa.Column('RESULTADO', sa.Boolean(), nullable=False),
        sa.Column('DAT_PUBL', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('ID'),
        sa.UniqueConstraint('NUM_AI')
    )

    # Seed initial data for operadora
    operadora_table = sa.table(
        'operadora',
        sa.column('ID', sa.Integer),
        sa.column('NOME', sa.String),
        sa.column('CONCESSIONARIA', sa.String)
    )
    op.bulk_insert(operadora_table, [
        {'ID': 107, 'NOME': 'MILENIO TRANSPORTES', 'CONCESSIONARIA': 'CONSORCIO PAMPULHA'},
        {'ID': 123, 'NOME': 'BOA VISTA COLETIVOS', 'CONCESSIONARIA': 'CONSORCIO BHLESTE'},
        {'ID': 113, 'NOME': 'VIA BH COLETIVOS', 'CONCESSIONARIA': 'CONSORCIO DEZ'},
        {'ID': 37, 'NOME': 'VIACAO ANCHIETA', 'CONCESSIONARIA': 'CONSORCIO DOM PEDRO II'}
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('recurso_segunda_instancia')
    op.drop_table('recurso_primeira_instancia')
    op.drop_table('auto_infracao')
    op.drop_table('linha')
    op.drop_table('veiculos')
    op.drop_table('operadora')
