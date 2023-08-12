"""add_column_completed_tasks_completed

Revision ID: 5c25f96f84a2
Revises: 428a49e81f42
Create Date: 2023-08-12 16:17:44.016970

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '5c25f96f84a2'
down_revision = '428a49e81f42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE `completed_tasks` ADD COLUMN `completed` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER `execution_time`;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE `completed_tasks` DROP COLUMN `completed`;
    """)
