import io
from os import error
import pandas as pd
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from akira_apps.faculty.forms import CreateUserForm, StudentsForm
from akira_apps.student.models import Students

# Create your views here.
def faculty_dashboard(request):
    return render(request, 'faculty/dashboard.html')

def add_student(request):
    form = CreateUserForm()
    student_form = StudentsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        student_form = StudentsForm(request.POST,request.FILES)

        if form.is_valid() and student_form.is_valid():
            user = form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = AuthenticationForm(username = username, password = password)

            group = Group.objects.get(name='Student')
            user.groups.add(group)

            return redirect('manage_student')
        else:
            form = CreateUserForm()
            student_form = StudentsForm()

    context = {'form':form, 'student_form':student_form}        
    return render(request, "oncl_app/admin_templates/student_templates/add_student.html", context)

def bulk_upload_students_save(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['studentfile'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in student_user and str(row['Email']) not in student_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    password=row['Password'],
                )
                Student=Group.objects.get(name='Student')
                if row['Group'] == 'Student':
                    Student.user_set.add(newuser)
                    newuser.groups.add(Student)

                student = Students.objects.bulk_create([
                    Students(
                        user_id = newuser.id,
                        gender=row['Gender'],
                        father_name=row['Father Name'],
                        father_occ=row['Father Occupation'],
                        father_phone=row['Father Phone'],
                        mother_name=row['Mother Name'],
                        mother_tounge=row['Mother Tounge'],
                        dob=(row['Date of Birth'] if row['Date of Birth'] != '' else '1998-12-01'),
                        blood_group=row['Blood Group'],
                        phone=row['Phone'],
                        dno_sn=row['Door No.'],
                        zip_code=row['Zip Code'],
                        city_name=row['City Name'],
                        state_name=row['State Name'],
                        country_name=row['Country'],
                        branch=row['Branch']
                    )
                ])
        success_message = "Student Record(s) Imported Successfully."
        context = {
            "success_message":success_message
        }
        return redirect('manage_student', context)
    else:
        error_message = "Failed to Import Bulk Records!."
        context = {
            "error_message":error_message
        }
        return redirect('manage_student', context)