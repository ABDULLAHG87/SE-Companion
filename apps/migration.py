from alembic import op
import sqlalchemy as sa

def upgrade():
    op.alter_column('users', 'password_hash', type_=sa.String(length=255))

def downgrade():
    op.alter_column('users', 'password_hash', type_=sa.String(length=100))  # Change the length as per your original schema
