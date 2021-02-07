from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, PasswordField, BooleanField,SelectField
from wtforms.validators import DataRequired, Email, URL, Length, Optional, ValidationError
from JiaLog.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit =SubmitField('Log in')


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.category.choices = \
            [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1,30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1,254)])
    site = StringField('Site', validators=[DataRequired(), URL(), Length(0,255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    my_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    my_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()