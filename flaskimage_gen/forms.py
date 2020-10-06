from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class YoutubeURLForm(FlaskForm):
    url = StringField('YoutubeURL',validators=[DataRequired(), Length(min=15, max=500)])
    # frame_rate = DecimalField('FrameRate', validators=[Optional(),NumberRange(min=100, max=500)])
    radio_out = RadioField('Output Format', choices=[('0', 'Image'), ('1', 'Audio'), ('2', 'Video'), ('3','Text')],
                           validators=[DataRequired()])
    submit = SubmitField('Process Video')
