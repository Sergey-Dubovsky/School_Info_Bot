"""log

Revision ID: f663391c9ad2
Revises: 383b35f8e826
Create Date: 2022-09-12 17:28:12.991203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f663391c9ad2'
down_revision = '383b35f8e826'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('info', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Numeric(precision=10, scale=0), nullable=False),
    sa.Column('user_firstname', sa.String(length=25), nullable=False),
    sa.Column('user_lastname', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logs_datetime'), 'logs', ['datetime'], unique=False)
    op.create_index(op.f('ix_logs_info'), 'logs', ['info'], unique=False)
    op.create_index(op.f('ix_logs_user_firstname'), 'logs', ['user_firstname'], unique=False)
    op.create_index(op.f('ix_logs_user_id'), 'logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_logs_user_lastname'), 'logs', ['user_lastname'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_logs_user_lastname'), table_name='logs')
    op.drop_index(op.f('ix_logs_user_id'), table_name='logs')
    op.drop_index(op.f('ix_logs_user_firstname'), table_name='logs')
    op.drop_index(op.f('ix_logs_info'), table_name='logs')
    op.drop_index(op.f('ix_logs_datetime'), table_name='logs')
    op.drop_table('logs')
    # ### end Alembic commands ###