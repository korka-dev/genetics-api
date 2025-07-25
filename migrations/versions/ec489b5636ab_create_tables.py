"""create tables

Revision ID: ec489b5636ab
Revises: 
Create Date: 2025-07-14 13:55:57.014968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec489b5636ab'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=False),
    sa.Column('otp_code', sa.String(length=6), nullable=True),
    sa.Column('otp_expires_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('incidents',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('priority', sa.Enum('FAIBLE', 'MOYENNE', 'HAUTE', 'CRITIQUE', name='priority'), nullable=False),
    sa.Column('category', sa.Enum('RESEAU', 'SECURITE', 'LOGICIEL', 'MATERIEL', 'ACCES', 'SURVEILLANCE', 'AUTRE', name='category'), nullable=False),
    sa.Column('status', sa.Enum('EN_ATTENTE', 'EN_TRAITEMENT', 'TERMINE', name='incidentstatus'), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('incidents')
    op.drop_table('users')
    # ### end Alembic commands ###
