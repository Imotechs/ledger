from django import forms
from .models import Record,Semester,Student

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
                fields ='__all__'
