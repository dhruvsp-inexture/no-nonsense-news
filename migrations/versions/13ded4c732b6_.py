"""empty message

Revision ID: 13ded4c732b6
Revises: 
Create Date: 2022-06-22 17:13:14.775831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13ded4c732b6'
down_revision = None
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
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('checked', sa.Boolean(), nullable=True),
    sa.Column('scraped_data', sa.Boolean(), nullable=True),
    sa.Column('news_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['news_category_id'], ['news_category.category_id'], ),
    sa.PrimaryKeyConstraint('news_id')
    )
    op.create_table('journalist_news_mapping',
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
    sa.PrimaryKeyConstraint('news_id', 'image')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news_image_mapping')
    op.drop_table('journalist_news_mapping')
    op.drop_table('news')
    op.drop_table('news_category')
    # ### end Alembic commands ###
