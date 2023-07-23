"""create_users

Revision ID: 8d0d6d9e95fc
Revises: 
Create Date: 2023-07-23 23:01:14.452751

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '8d0d6d9e95fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE `users` (
            `ID` INT(10) NOT NULL AUTO_INCREMENT,
            `email` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
            `encrypted_password` VARCHAR(128) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
            PRIMARY KEY (`ID`) USING BTREE,
            UNIQUE INDEX `email` (`email`) USING BTREE
        )
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE users;
    """)
