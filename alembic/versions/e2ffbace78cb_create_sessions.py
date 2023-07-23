"""create_sessions

Revision ID: e2ffbace78cb
Revises: 8d0d6d9e95fc
Create Date: 2023-07-23 23:14:03.514428

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e2ffbace78cb'
down_revision = '8d0d6d9e95fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE `sessions` (
            `ID` INT(10) NOT NULL AUTO_INCREMENT,
            `user` INT(10) NOT NULL,
            `refresh_token` VARCHAR(300) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
            `created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `reseted` TINYINT(3) NOT NULL DEFAULT '0',
            PRIMARY KEY (`ID`) USING BTREE,
            INDEX `FK_sessions_users` (`user`) USING BTREE,
            INDEX `refresh_token` (`refresh_token`) USING BTREE
        )
    """)
    pass


def downgrade() -> None:
    op.execute("""
        DROP TABLE sessions;
    """)
    pass
