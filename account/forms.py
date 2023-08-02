from django import forms
from .models import Record,Semester,Student,Department

class SemesterForm(forms.Form):
        semester = (
                ("First","First"),
                ("Second","Second")
                    )    
        semester = forms.ChoiceField(choices=semester,initial="First")

class SessionForm(forms.Form):
        session = (
        ("2020/2021","2020/2021"),
        ("2021/2022","2021/2022"),
        ("2022/2023","2022/2023"),
      
    )
        
        session = forms.ChoiceField(choices=session,initial="2020/2021")

class StudentForm(forms.ModelForm):
        class Meta:
                model = Student
                fields =['reg_no','first_name','middle_name','level','last_name','course_option']

        def department(self):
                choice =  Department.objects.all()
                #print(choice,type(choice))
                return choice
