from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length


class PostArticlesForm(FlaskForm):
    """form for posting articles for journalist

     Attributes
    ----------
    title: str
        contains the title of the article to be posted
    content: str
        contains the content of the article to be posted
    """
    title = StringField('Title', validators=[DataRequired(), Length(min=10, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Post')


class ArticlesImageUploadForm(FlaskForm):
    """forms for posting multiple images

     Attributes
    ----------
    picture: button
        button for uploading multiple files while posting articles
    """

    picture = MultipleFileField('Upload Images')


class UpdateArticlesForm(FlaskForm):
    """form for updating articles posted by journalist

     Attributes
    ----------
    title: str
        contains the title of the article which is being updated
    content: str
        contains the content of the article which is being updated
    """

    title = StringField('Title', validators=[DataRequired(), Length(min=10, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    picture = MultipleFileField('Upload Images')

    submit = SubmitField('Update')


class UploadFileForm(FlaskForm):
    """form for uploading files

     Attributes
    ----------
    picture: button
        button for uploading multiple files while updating the article
    """

    picture = MultipleFileField('Upload Images')
    submit = SubmitField('Upload')
