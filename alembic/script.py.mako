"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    op.execute("""
        // sql code here
    """)
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    op.execute("""
        // sql code here
    """)
    ${downgrades if downgrades else "pass"}
