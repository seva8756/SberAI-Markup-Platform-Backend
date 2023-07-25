"""add_column_users_isAdmin

Revision ID: 57bb4e4416d9
Revises: dc72b2f73397
Create Date: 2023-07-24 17:50:14.714385

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '57bb4e4416d9'
down_revision = 'dc72b2f73397'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE `users` ADD COLUMN `isAdmin` TINYINT(3) NOT NULL DEFAULT '0' AFTER `encrypted_password`;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE `users` DROP COLUMN `isAdmin`;
    """)
    pass
