def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('stadium',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('turf_type', sa.String(), nullable=True),
        sa.Column('year_built', sa.Integer(), nullable=True),
        sa.Column('altitude', sa.Integer(), nullable=True),
        sa.Column('dome', sa.Boolean(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stadium_id'), 'stadium', ['id'], unique=False)
    op.create_index(op.f('ix_stadium_name'), 'stadium', ['name'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_stadium_name'), table_name='stadium')
    op.drop_index(op.f('ix_stadium_id'), table_name='stadium')
    op.drop_table('stadium')