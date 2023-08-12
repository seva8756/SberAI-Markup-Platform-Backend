"""add_column_compl_tasks_answer_extended

Revision ID: 5007b0b4c92a
Revises: 5c25f96f84a2
Create Date: 2023-08-12 20:51:38.648899

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '5007b0b4c92a'
down_revision = '5c25f96f84a2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE `completed_tasks` ADD COLUMN `answer_extended` MEDIUMTEXT NOT NULL AFTER `answer`;
    """)
    op.execute("""
           ALTER TABLE `completed_tasks` CHANGE COLUMN `answer` `answer` MEDIUMTEXT NOT NULL COLLATE 'utf8mb4_0900_ai_ci' AFTER `task`;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE `completed_tasks` DROP COLUMN `answer_extended`;
    """)
    op.execute("""
        ALTER TABLE `completed_tasks` CHANGE COLUMN `answer` `answer` TEXT NOT NULL COLLATE 'utf8mb4_0900_ai_ci' AFTER `task`;
    """)
