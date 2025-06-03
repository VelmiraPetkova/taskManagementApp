from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '4b4e00aa15db'
down_revision = '4b4e00aa15db'

def upgrade():
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.drop_constraint('tasks_ibfk_1', type_='foreignkey')  # провери името!
        batch_op.alter_column(
            'user_id',
            existing_type=sa.BINARY(16),
            type_=sa.String(36),
            existing_nullable=True
        )
        batch_op.create_foreign_key(
            'tasks_user_id_fkey',
            'users',
            ['user_id'],
            ['id']
        )

    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.BINARY(16),
            type_=sa.String(36),
            existing_nullable=False
        )

def downgrade():
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.drop_constraint('tasks_user_id_fkey', type_='foreignkey')
        batch_op.alter_column(
            'user_id',
            existing_type=sa.String(36),
            type_=sa.BINARY(16),
            existing_nullable=True
        )
        batch_op.create_foreign_key(
            'tasks_ibfk_1',
            'users',
            ['user_id'],
            ['id']
        )

    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.String(36),
            type_=sa.BINARY(16),
            existing_nullable=False
        )
