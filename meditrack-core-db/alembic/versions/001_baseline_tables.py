"""baseline migration for core tables

Revision ID: 001_baseline
Create Date: 2026-09-04
"""
from alembic import op
import sqlalchemy as sa

revision = '001_baseline'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Departments
    op.create_table(
        'departments',
        sa.Column('department_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    # Staff
    op.create_table(
        'staff',
        sa.Column('staff_id', sa.Integer, primary_key=True),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.department_id', ondelete='RESTRICT'), nullable=False),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    # Appointments
    op.create_table(
        'appointments',
        sa.Column('appointment_id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False),
        sa.Column('staff_id', sa.Integer, sa.ForeignKey('staff.staff_id', ondelete='RESTRICT'), nullable=False),
        sa.Column('scheduled_time', sa.TIMESTAMP, nullable=False),
        sa.Column('status', sa.String(20), server_default='SCHEDULED', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('appointments')
    op.drop_table('staff')
    op.drop_table('departments')
