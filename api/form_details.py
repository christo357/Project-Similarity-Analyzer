from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired

# Create a WTForms form class
class ResultForm(FlaskForm):
    result_value = HiddenField('Result Value', validators=[DataRequired()])
    submit = SubmitField('DETAILS')



