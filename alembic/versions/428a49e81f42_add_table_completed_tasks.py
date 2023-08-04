"""add_table_completed_tasks

Revision ID: 428a49e81f42
Revises: e72e01d902fa
Create Date: 2023-08-04 20:31:23.071161

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '428a49e81f42'
down_revision = 'e72e01d902fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE `completed_tasks` (
            `ID` INT(10) NOT NULL AUTO_INCREMENT,
            `user` INT(10) NOT NULL,
            `project` INT(10) NOT NULL,
            `task` INT(10) NOT NULL,
            `answer` TEXT NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
            `execution_time` INT(10) NOT NULL DEFAULT '0',
            PRIMARY KEY (`ID`) USING BTREE
        )
    """)
    pass


def downgrade() -> None:
    op.execute("""
        DROP TABLE completed_tasks;
    """)
    pass
