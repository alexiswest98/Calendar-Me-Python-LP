from flask_wtf import FlaskForm

from wtforms.fields import (StringField, DateField, TimeField, TextAreaField,
                            BooleanField, SubmitField)

from wtforms.validators import (DataRequired, ValidationError)

from datetime import datetime

def validate_dates(form, field):
    start_date1 = form.start_date.data
    end_date1 = field.data

    if start_date1 != end_date1:
        msg2 = "Start date and End date have to be on the same day"
        raise ValidationError(msg2)

class AppointmentForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    start_date = DateField("start_date", validators=[DataRequired()])
    start_time = TimeField("start_time", validators=[DataRequired()])
    end_date = DateField("end_date", validators=[DataRequired(), validate_dates])
    end_time = TimeField("end_time", validators=[DataRequired()])
    description = TextAreaField("description", validators=[DataRequired()])
    private = BooleanField("private")
    submit = SubmitField("Create appointment")

    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(field.data, form.end_time.data)

        if start >= end:
            msg = "End date/time must come after start date/time"
            raise ValidationError(msg)

    
