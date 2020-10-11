from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
import re

from app.models import User


class EditToolForm(FlaskForm):
    toolname=StringField("Tool Name", validators=[DataRequired()])
    category=SelectField(
        "Category",
        choices=[('Data', 'Data'), ("Metrics", "Metrics"), ("Modeling", "Modeling")],
        validators=[DataRequired()]
    )
    owner1=StringField("Owner 1", validators=[DataRequired()])
    owner2=StringField("Owner 2")
    owner3=StringField("Owner 3")
    about=StringField("About", validators=[DataRequired()])
    submit=SubmitField("Apply Changes")

    @staticmethod
    def trim_toolname(toolname):
        trimmed_toolname=re.sub(r"([^A-Za-z0-9])+","-", toolname).lower()
        # re.findall(r"[A-Za-z0-9]+", "Data_!!Foundry")
        return(trimmed_toolname)

class DeleteToolButton(FlaskForm):
    delete=SubmitField("Delete Tool")

class DeleteToolForm(FlaskForm):
    toolname=StringField("Are you sure? Enter the tool name as it appears above:")
    submit=SubmitField("Delete")
