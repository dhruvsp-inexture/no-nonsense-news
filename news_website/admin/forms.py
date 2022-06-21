from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

from news_website.admin.utils import check_category


class addCategoryForm(FlaskForm):
    """class for creating form for adding category"""
    news_type = StringField('Add New Category', validators=[Length(min=2, max=20), check_category])
    submit = SubmitField('Add')

