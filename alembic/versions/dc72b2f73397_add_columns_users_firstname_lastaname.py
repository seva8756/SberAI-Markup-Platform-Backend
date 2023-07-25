"""add_columns_users_firstname_lastaname

Revision ID: dc72b2f73397
Revises: e2ffbace78cb
Create Date: 2023-07-24 17:49:04.535448

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dc72b2f73397'
down_revision = 'e2ffbace78cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE `users` ADD COLUMN `firstName` VARCHAR(50) NOT NULL AFTER `email`;
    """)
    op.execute("""
        ALTER TABLE `users` ADD COLUMN `lastName` VARCHAR(50) NOT NULL AFTER `firstName`;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE `users` DROP COLUMN `firstName`;
    """)
    op.execute("""
        ALTER TABLE `users` DROP COLUMN `lastName`;
    """)
