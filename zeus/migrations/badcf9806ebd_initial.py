"""initial

Revision ID: badcf9806ebd
Revises:
Create Date: 2017-07-04 12:34:46.351762

"""
import zeus
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'badcf9806ebd'
down_revision = None
branch_labels = ('default', )
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'author',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email')
    )
    op.create_table(
        'itemoption',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('item_id', zeus.db.types.GUID(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('item_id', 'name', name='unq_itemoption_name')
    )
    op.create_table(
        'repository',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('url', sa.String(length=200), nullable=False),
        sa.Column('backend', zeus.db.types.Enum(), nullable=False),
        sa.Column('status', zeus.db.types.Enum(), nullable=False),
        sa.Column('data', zeus.db.types.JSONEncodedDict(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('last_update', sa.DateTime(), nullable=True),
        sa.Column('last_update_attempt', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('url')
    )
    op.create_table(
        'user',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email')
    )
    op.create_table(
        'identity',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('user_id', zeus.db.types.GUID(), nullable=False),
        sa.Column('external_id', sa.String(length=64), nullable=False),
        sa.Column('provider', sa.String(length=32), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('config', zeus.db.types.JSONEncodedDict(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('external_id'),
        sa.UniqueConstraint('user_id', 'provider', name='unq_identity_user')
    )
    op.create_index(op.f('ix_identity_user_id'), 'identity', ['user_id'], unique=False)
    op.create_table(
        'patch',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('parent_revision_sha', sa.String(length=40), nullable=False),
        sa.Column('diff', sa.Text(), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('repository_id', zeus.db.types.GUID(), nullable=False),
        sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_repo_sha', 'patch', ['repository_id', 'parent_revision_sha'], unique=False)
    op.create_index(op.f('ix_patch_repository_id'), 'patch', ['repository_id'], unique=False)
    op.create_table(
        'revision',
        sa.Column('sha', sa.String(length=40), nullable=False),
        sa.Column('author_id', zeus.db.types.GUID(), nullable=True),
        sa.Column('committer_id', zeus.db.types.GUID(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('parents', postgresql.ARRAY(sa.String(length=40)), nullable=True),
        sa.Column('branches', postgresql.ARRAY(sa.String(length=128)), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('date_committed', sa.DateTime(), nullable=True),
        sa.Column('repository_id', zeus.db.types.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ['author_id'],
            ['author.id'],
        ),
        sa.ForeignKeyConstraint(
            ['committer_id'],
            ['author.id'],
        ),
        sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('sha'),
        sa.UniqueConstraint('repository_id', 'sha', name='unq_revision')
    )
    op.create_index(op.f('ix_revision_author_id'), 'revision', ['author_id'], unique=False)
    op.create_index(op.f('ix_revision_committer_id'), 'revision', ['committer_id'], unique=False)
    op.create_index(op.f('ix_revision_repository_id'), 'revision', ['repository_id'], unique=False)
    op.create_table(
        'source',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('patch_id', zeus.db.types.GUID(), nullable=True),
        sa.Column('revision_sha', sa.String(length=40), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('data', zeus.db.types.JSONEncodedDict(), nullable=True),
        sa.Column('repository_id', zeus.db.types.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ['patch_id'],
            ['patch.id'],
        ),
        sa.ForeignKeyConstraint(
            ['repository_id', 'revision_sha'],
            ['revision.repository_id', 'revision.sha'],
        ),
        sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('patch_id'),
        sa.UniqueConstraint(
            'repository_id', 'revision_sha', 'patch_id', name='unq_source_revision'
        )
    )
    op.create_index(
        'idx_source_repo_sha', 'source', ['repository_id', 'revision_sha'], unique=False
    )
    op.create_index(op.f('ix_source_repository_id'), 'source', ['repository_id'], unique=False)
    op.create_table(
        'build',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('source_id', zeus.db.types.GUID(), nullable=False),
        sa.Column('status', zeus.db.types.Enum(), nullable=False),
        sa.Column('result', zeus.db.types.Enum(), nullable=False),
        sa.Column('date_started', sa.DateTime(), nullable=True),
        sa.Column('date_finished', sa.DateTime(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('data', zeus.db.types.JSONEncodedDict(), nullable=True),
        sa.Column('repository_id', zeus.db.types.GUID(), nullable=False),
        sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_id'], ['source.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_build_repository_id'), 'build', ['repository_id'], unique=False)
    op.create_index(op.f('ix_build_source_id'), 'build', ['source_id'], unique=False)
    op.create_table(
        'job',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('build_id', zeus.db.types.GUID(), nullable=False),
        sa.Column('status', zeus.db.types.Enum(), nullable=False),
        sa.Column('result', zeus.db.types.Enum(), nullable=False),
        sa.Column('date_started', sa.DateTime(), nullable=True),
        sa.Column('date_finished', sa.DateTime(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('data', zeus.db.types.JSONEncodedDict(), nullable=True),
        sa.Column('repository_id', zeus.db.types.GUID(), nullable=False),
        sa.ForeignKeyConstraint(['build_id'], ['build.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_build_id'), 'job', ['build_id'], unique=False)
    op.create_index(op.f('ix_job_repository_id'), 'job', ['repository_id'], unique=False)
    op.create_table(
        'testcase',
        sa.Column('id', zeus.db.types.GUID(), nullable=False),
        sa.Column('job_id', zeus.db.types.GUID(), nullable=False),
        sa.Column('hash', sa.String(length=40), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('result', zeus.db.types.Enum(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('repository_id', zeus.db.types.GUID(), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['job.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('job_id', 'hash', name='unq_testcase_hash')
    )
    op.create_index(op.f('ix_testcase_repository_id'), 'testcase', ['repository_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_testcase_repository_id'), table_name='testcase')
    op.drop_table('testcase')
    op.drop_index(op.f('ix_job_repository_id'), table_name='job')
    op.drop_index(op.f('ix_job_build_id'), table_name='job')
    op.drop_table('job')
    op.drop_index(op.f('ix_build_source_id'), table_name='build')
    op.drop_index(op.f('ix_build_repository_id'), table_name='build')
    op.drop_table('build')
    op.drop_index(op.f('ix_source_repository_id'), table_name='source')
    op.drop_index('idx_source_repo_sha', table_name='source')
    op.drop_table('source')
    op.drop_index(op.f('ix_revision_repository_id'), table_name='revision')
    op.drop_index(op.f('ix_revision_committer_id'), table_name='revision')
    op.drop_index(op.f('ix_revision_author_id'), table_name='revision')
    op.drop_table('revision')
    op.drop_index(op.f('ix_patch_repository_id'), table_name='patch')
    op.drop_index('idx_repo_sha', table_name='patch')
    op.drop_table('patch')
    op.drop_index(op.f('ix_identity_user_id'), table_name='identity')
    op.drop_table('identity')
    op.drop_table('user')
    op.drop_table('repository')
    op.drop_table('itemoption')
    op.drop_table('author')
    # ### end Alembic commands ###
