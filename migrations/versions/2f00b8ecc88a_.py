"""empty message

Revision ID: 2f00b8ecc88a
Revises: 
Create Date: 2024-11-12 02:25:00.420535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f00b8ecc88a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('room_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('status_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.alter_column('passport_number',
               existing_type=sa.CHAR(length=9),
               type_=sa.String(length=9),
               nullable=False)
        batch_op.alter_column('phone_number',
               existing_type=sa.CHAR(length=13),
               type_=sa.String(length=13),
               nullable=False)

    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.alter_column('number',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('bed_capacity',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('price_per_night',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               nullable=False)

    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               nullable=True)

    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.alter_column('price_per_night',
               existing_type=sa.NUMERIC(precision=7, scale=2),
               nullable=True)
        batch_op.alter_column('bed_capacity',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('number',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.String(length=13),
               type_=sa.CHAR(length=13),
               nullable=True)
        batch_op.alter_column('passport_number',
               existing_type=sa.String(length=9),
               type_=sa.CHAR(length=9),
               nullable=True)

    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('status_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('room_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
