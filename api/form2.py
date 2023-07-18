from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField,StringField
from wtforms.validators import DataRequired


class detailForm(FlaskForm):
  title = StringField("Title",validators=[DataRequired()])
  abstract = TextAreaField("Abstract", validators=[DataRequired()])
  submit = SubmitField("Add")