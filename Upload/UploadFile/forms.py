from django.db import models
from django import forms
from .models import MainPage
import datetime
from datetime import date

techlist = (
    ('DateOfDrive', 'DateOfDrive'),
    ('NameOfDrive', 'NameOfDrive'),
    ('Status', 'Status'),
    ('Marks_Scored', 'Marks_Scored'),
    ('First_Round_Interviewer_Name', 'First_Round_Interviewer_Name'),
    ('Second_Round_Interviewer_Name', 'Second_Round_Interviewer_Name'),
    ('Third_Round_Interviewer_Name', 'Third_Round_Interviewer_Name'),
    ('Management_Round_Interviewer_Name', 'Management_Round_Interviewer_Name'),
    ('HR_Round_Interviewer_Name', 'HR_Round_Interviewer_Name')
)

class UploadFileForm(forms.ModelForm):   # Class to make forms directly from the model: Main Page
    DateOfDrive = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y',), required=True)
    NameOfDrive = forms.CharField(required=True)

    class Meta:
        model = MainPage
        fields = ['DateOfDrive','NameOfDrive']


class analysisForm(forms.Form):

    GroupBy = forms.ChoiceField(choices=techlist)
    where = forms.CharField()
    datefrom = forms.DateField(initial="2019-01-01")
    dateto = forms.DateField(initial=date.today())


