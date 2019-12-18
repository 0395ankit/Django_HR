
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


class MainPage(models.Model):   # Model for storing the main page data.

    unique_id = models.AutoField(primary_key=True, unique=True)      # Primary key
    DateOfDrive = models.DateField(default='2019-01-01')
    NameOfDrive = models.CharField(max_length=100)

    class Meta:
        unique_together = ("DateOfDrive", "NameOfDrive")

    def __str__(self):
        return 'unique_id: {0} DateOfDrive: {1} NameOfDrive: {2}'.format(self.unique_id, self.DateOfDrive, self.NameOfDrive)


class Upload(models.Model):

    Student_Name = models.CharField(max_length=100, default="")
    Total_Marks = models.CharField(max_length=100, default="")
    Marks_Scored = models.CharField(max_length=100, default="")
    Status_value = (
        ('First', 'First round rejected '),
        ('Second', 'Second round rejected'),
        ('Third', 'Third round rejected'),
        ('Fourth', 'Written Test rejected '),
        ('Fifth', 'Drop out')
    )
    Status = models.CharField(max_length=100, default="")
    PhoneNumber = models.CharField(max_length=12, default=1)
    unique_id = models.IntegerField()  # Foreign Key to Main Page
    First_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    Second_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    Third_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    Management_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    HR_Round_Interviewer_Name = models.CharField(max_length=100, default="")

    def __str__(self):
        return 'Student Name: {0} Total Marks: {1} Marks Scored: {2} Status: {3} ' \
               'Phone Number: {4}'\
            .format(self.Student_Name, self.Total_Marks, self.Marks_Scored, self.Status,
                    self.PhoneNumber)


class Summary(models.Model):

    unique_id = models.AutoField(primary_key=True, unique=True)      # Primary key
    DateOfDrive = models.DateField(default='2019-01-01')
    NameOfDrive = models.CharField(max_length=100)
    Student_Name = models.CharField(max_length=100, default="")
    Marks_Scored = models.CharField(max_length=100, default="")
    Status = models.CharField(max_length=10, default="")
    PhoneNumber = models.CharField(max_length=12, default=1)
    First_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    Second_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    Third_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    Management_Round_Interviewer_Name = models.CharField(max_length=100, default="")
    HR_Round_Interviewer_Name = models.CharField(max_length=100, default="")

    class Meta:
        managed = False
        db_table = "UploadFile_summary"