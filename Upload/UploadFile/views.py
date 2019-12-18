from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django import forms
import django_excel as excel
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
from datetime import datetime
from django.views.generic import TemplateView, FormView
import pandas as pd
import csv
import os
import chart_studio.plotly as py
import plotly.figure_factory as ff
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import calendar
from django.db import connection


class UploadView(TemplateView):     # Template to use for the main screen
    template_name = 'upload_form.html'

    def get(self, request):     # Function to show the data on screen.
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):        # Function for posting the data to db

        form = UploadFileForm(request.POST)
        excel_file = request.FILES["excel_file"]        # File that is passed to the browse button
        df = pd.read_excel(excel_file, index=False)     # Creating the dataframe to append the ID column
        boolean_duplicate = any(df['Phone Number'].duplicated())        # Checking for the duplicate phone number
        boolean_null = df['Phone Number'].isnull().any()
        if boolean_duplicate == True or boolean_null == True:       # Checking the file for duplicate or null value in contact column
            return HttpResponse("Values in phone number column in file uploaded are either duplicate or empty.")

        else:
            if form.is_valid():
                data = request.POST.copy()      # Making copy of the data posted in the form
                Dateofdrive = data.get('DateOfDrive')       # Value of the date field from the form
                Nameofdrive = data.get('NameOfDrive')       # Value of the name field from the form
                value = date.today()                        # This variable is used to get today date to compare with the above date
                parsed_date = datetime.strptime(Dateofdrive, "%d/%m/%Y").strftime("%Y-%m-%d")
                boolean_name_of_drive = (MainPage.objects.filter(NameOfDrive= Nameofdrive).exists())    # To verify if the name already exists in db

                if parsed_date > str(value):        # To restrict the user from entering date greater than today.
                    return HttpResponse("Date cannot be future date")

                elif boolean_name_of_drive==True:  # Checking if the name already exists in DB, throw error

                    html = "<html><body>This entry already exists. </body></html>"
                    return HttpResponse(html)

                else:           # If everything is as per the requirement and different then make the entry in DB
                    idgen = form.save()
                    df['unikey'] = int(idgen.pk)            # Adding the column for the ID column in the uploaded file
                    df.to_csv('df.csv', header=True, index=False)       # Converting to CSV
                    db_name = "Upload"                  # Model to be used for insertion
                    with open('df.csv') as csvfile:         # Reading the CSV to the model DB
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            p = Upload(Student_Name=row['Student Name'], Total_Marks=row['Total Marks'], Marks_Scored=row['Marks Scored'],
                                       Status=row['Status'], PhoneNumber=row['Phone Number'], unique_id=row['unikey'], First_Round_Interviewer_Name=row['1st  Round Interviewer Name'], Second_Round_Interviewer_Name=row['2nd Round Interviewer Name'],
                                       Third_Round_Interviewer_Name=row['Third Round Interviewer Name '], Management_Round_Interviewer_Name=row['Management/HR Round Interviewer Name'], HR_Round_Interviewer_Name=row['HR Round '])
                            p.save()        # Saving each record of the file using instance of the Uplaod model
            else:
                return HttpResponse('Entry already exists')
                form = UploadFileForm()
            return HttpResponse('OK')
                #return render(request, 'index.html', {"excel_data": excel_data})
                #return render(request, self.template_name,{'form': form})


class analysis(FormView):
    template_name = 'analysis.html'
# View for the analysis page

    def get(self, request):
        form = analysisForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = analysisForm(request.POST)
        if form.is_valid():
            groupbyf = form.cleaned_data['GroupBy']     # Getting the groupby otpion from the user
            wheref = form.cleaned_data['where']  # Getting the search element from the user
            datetof = form.cleaned_data['dateto']       # Getting the end date from the user
            datefromf = form.cleaned_data['datefrom']   # Getting the from date from the user

            list_of_where = list(wheref.split(','))
            print(list_of_where)


            # Loading the excel to data frame
            query = str(Summary.objects.all().query)
            df_view_summary = pd.read_sql_query(query, connection)
            print(df_view_summary)

            # Extracting the month number from the complete date
            df_view_summary['Month'] = pd.DatetimeIndex(df_view_summary['DateOfDrive']).month
            df_view_summary['Month'] = df_view_summary['Month'].apply(lambda x: calendar.month_abbr[x])

            # Data frame for all the month names.
            df2 = pd.DataFrame({'month': list(range(1, 13))})

            # Converting the month number to name.
            df2['Month'] = df2['month'].apply(lambda x: calendar.month_abbr[x])
            result_df_interview_month = pd.merge(df_view_summary, df2, how='outer')
            result_df_interview_month['DateOfDrive'] = pd.to_datetime(result_df_interview_month['DateOfDrive'])
            result_df_interview_month['DateOfDrive'] = result_df_interview_month['DateOfDrive'].dt.date

            # Filtering data based on the from and to date given by the user
            mask = (result_df_interview_month['DateOfDrive'] >= datefromf) & (result_df_interview_month['DateOfDrive'] <= datetof)
            date_filterd_df = result_df_interview_month.loc[mask]

            # Grouping the data based on the field passed by the user and date of drive column
            count_list=[]
            unique_val=[]
            unique_date=[]
            if groupbyf == 'DateOfDrive':
                grouped = date_filterd_df.groupby(['DateOfDrive'], as_index=False).count()
                count_list = grouped['unique_id'].tolist()  # List containing count of entries
                unique_val = grouped[groupbyf].unique().tolist()  # List containing name of key, for column name passed by user

                # Getting unique keys from the data frame
                # (One from the column chosen by the user and the other from the dates column)
                unique_date = date_filterd_df['DateOfDrive'].unique().tolist()
                unique_key_ = date_filterd_df[groupbyf].unique().tolist()

                # Creating a json format of the data based on the request
                data = []
                data_date = []

                for date in unique_date:
                    for elements, val in zip(unique_val, count_list):
                        if {'count': val} not in data_date:
                            data_date.append({'count': val})
                    data.append({str(date): data_date})
                    data_date = []
                unique_date=[]
            else:
                grouped = date_filterd_df.groupby(['DateOfDrive', groupbyf], as_index=False).count()
                count_list = grouped['unique_id'].tolist()  # List containing count of entries
                unique_val = grouped[groupbyf].unique().tolist()     # List containing name of key,for column name passed by user
                while "" in unique_val:
                    unique_val.remove("")

                    # Getting unique keys from the data frame
                # (One from the column chosen by the user and the other from the dates column)
                unique_date = date_filterd_df['DateOfDrive'].unique().tolist()
                unique_key_ = date_filterd_df[groupbyf].unique().tolist()

                # Creating a json format of the data based on the request
                data=[]
                data_date=[]

                for date in unique_date:
                    for elements, val in zip(unique_val, count_list):
                        if {groupbyf: elements, 'count': val} not in data_date:
                            data_date.append({groupbyf: elements, 'count': val})
                    data.append({str(date): data_date})
                    data_date = []
                unique_date=[]
            print(data)
            return JsonResponse(data, safe=False)
