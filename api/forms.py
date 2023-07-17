from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class abstractForm(FlaskForm):
  abstract = TextAreaField("Abstract", validators=[DataRequired()])
  submit = SubmitField("CHECK")