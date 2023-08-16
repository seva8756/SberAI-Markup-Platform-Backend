"""add_column_users_regip_and_regdate

Revision ID: 661b723841b5
Revises: 5007b0b4c92a
Create Date: 2023-08-16 14:57:25.741793

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '661b723841b5'
down_revision = '5007b0b4c92a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE `users` ADD COLUMN `reg_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() AFTER `isAdmin`;
    """)
    op.execute("""
        ALTER TABLE `users` ADD COLUMN `reg_ip` VARCHAR(50) NOT NULL AFTER `isAdmin`;
    """)


def downgrade() -> None:
    op.execute("""
         ALTER TABLE `completed_tasks` DROP COLUMN `reg_date`;
    """)
    op.execute("""
             ALTER TABLE `completed_tasks` DROP COLUMN `reg_ip`;
    """)
