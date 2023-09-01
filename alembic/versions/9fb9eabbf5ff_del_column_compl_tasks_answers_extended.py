"""del_column_compl_tasks_answers_extended

Revision ID: 9fb9eabbf5ff
Revises: 661b723841b5
Create Date: 2023-08-30 17:08:12.551438

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '9fb9eabbf5ff'
down_revision = '661b723841b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE `completed_tasks` DROP COLUMN `answer_extended`;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE `completed_tasks` ADD COLUMN `answer_extended` MEDIUMTEXT NOT NULL AFTER `answer`;
    """)
