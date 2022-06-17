"""empty message

Revision ID: 79aad3415367
Revises: dc28f9db60d1
Create Date: 2022-06-14 11:56:06.661817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79aad3415367'
down_revision = 'dc28f9db60d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news_category',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('category_id'),
    sa.UniqueConstraint('category')
    )
    op.create_table('news',
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('news_heading', sa.String(), nullable=False),
    sa.Column('news_info', sa.String(), nullable=False),
    sa.Column('news_date', sa.DateTime(), nullable=True),
    sa.Column('news_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['news_category_id'], ['news_category.category_id'], ),
    sa.PrimaryKeyConstraint('news_id')
    )
    op.create_table('doc_speciality',
    sa.Column('journalist_id', sa.Integer(), nullable=False),
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['journalist_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['news_id'], ['news.news_id'], ),
    sa.PrimaryKeyConstraint('journalist_id', 'news_id')
    )
    op.create_table('news_image_mapping',
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['news_id'], ['news.news_id'], ),
    sa.PrimaryKeyConstraint('news_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news_image_mapping')
    op.drop_table('doc_speciality')
    op.drop_table('news')
    op.drop_table('news_category')
    # ### end Alembic commands ###
