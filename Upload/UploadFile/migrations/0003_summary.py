# Generated by Django 2.2.7 on 2019-12-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadFile', '0002_auto_20191210_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('unique_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('DateOfDrive', models.DateField(default='2019-01-01')),
                ('NameOfDrive', models.CharField(max_length=100)),
                ('Student_Name', models.CharField(default='', max_length=100)),
                ('Marks_Scored', models.CharField(default='', max_length=100)),
                ('Status', models.CharField(default='', max_length=10)),
                ('PhoneNumber', models.CharField(default=1, max_length=12)),
                ('First_Round_Interviewer_Name', models.CharField(default='', max_length=100)),
                ('Second_Round_Interviewer_Name', models.CharField(default='', max_length=100)),
                ('Third_Round_Interviewer_Name', models.CharField(default='', max_length=100)),
                ('Management_Round_Interviewer_Name', models.CharField(default='', max_length=100)),
                ('HR_Round_Interviewer_Name', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'UploadFile_summary',
                'managed': False,
            },
        ),
    ]
