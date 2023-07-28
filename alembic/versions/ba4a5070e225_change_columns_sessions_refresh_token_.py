"""change_columns_sessions_refresh_token_length

Revision ID: ba4a5070e225
Revises: 57bb4e4416d9
Create Date: 2023-07-29 00:50:58.169568

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ba4a5070e225'
down_revision = '57bb4e4416d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE `sessions`
        CHANGE COLUMN `refresh_token` `refresh_token` VARCHAR(330) NOT NULL COLLATE 'utf8mb4_0900_ai_ci' AFTER `user`;
    """)
    pass


def downgrade() -> None:
    op.execute("""
        ALTER TABLE `sessions`
        CHANGE COLUMN `refresh_token` `refresh_token` VARCHAR(300) NOT NULL COLLATE 'utf8mb4_0900_ai_ci' AFTER `user`;
    """)
    pass
