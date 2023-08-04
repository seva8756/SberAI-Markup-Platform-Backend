"""add_table_projects_and_participants

Revision ID: e72e01d902fa
Revises: ba4a5070e225
Create Date: 2023-07-29 14:07:25.717395

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e72e01d902fa'
down_revision = 'ba4a5070e225'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE `projects` (
            `ID` INT(10) NOT NULL AUTO_INCREMENT,
            `directory` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
            `closed` TINYINT(3) NOT NULL DEFAULT '0',
            `deleted` TINYINT(3) NOT NULL DEFAULT '0',
            PRIMARY KEY (`ID`) USING BTREE
        )
    """)
    op.execute("""
        CREATE TABLE `projects_participants` (
            `ID` INT(10) NOT NULL AUTO_INCREMENT,
            `project` INT(10) NOT NULL,
            `user` INT(10) NOT NULL,
            `joined` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`ID`) USING BTREE
        )
    """)
    pass


def downgrade() -> None:
    op.execute("""
        DROP TABLE projects;
    """)
    op.execute("""
        DROP TABLE projects_participants;
    """)
    pass
