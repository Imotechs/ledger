from typing import Any, Dict, Optional
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import SemesterForm,SessionForm,StudentForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,DetailView
from django.contrib.auth import get_user_model
from .models import Student,Record,Semester,Session,Department
from django.utils.http import urlencode
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Q



adminusername = '.'
pass_keys= 'admin123'
def my_custom_error_view(request):
    return render(request,'500.html')

def page_not_found_view(request):
    return render(request,'404.html')

def page_restricted_view(request):
    return render(request,'403.html')

def get_url(para):
    url = urlencode({'arg':para})
    return url

def description(request):
    return render(request,'description.html')
User = get_user_model()

# Create your views here.
@login_required
def home(request):
    records = Record.objects.filter(is_draft = False)
    if request.method =="POST":
        search = request.POST['search']
        if search is not None:
            searches =Record.objects.filter(Q(reg_no__icontains=search) | Q(session__session_name__icontains=search) | Q(reciept_no__icontains=search))
            context = {
                'records':searches
                }
            return render(request,'home.html',context)

    context = {
        'records':records
    }
    return render(request,'home.html',context)

@login_required
def add_record(request,*args,**kwargs):
    pk = kwargs.get('pk')
    student_reg = None
    if pk:
        student_reg = Student.objects.get(id = pk).reg_no
    
    if request.method=="POST":
        ammount_due = float(request.POST['ammount_due'])
        paid = float(request.POST['paid'])
        reg_no= request.POST['reg_no']
        session = Session.objects.get(session_name =request.POST['session'])
        obj = Record(
        semester= Semester.objects.get(semester_name=request.POST['semester'],session=session),
        item = request.POST['item'],
        session = session,
        reciept_no =request.POST['reciept_no'],
        ammount_due = ammount_due,
        paid = paid,
        reg_no=reg_no,
        )
        obj.balance = ammount_due-paid

        if Student.objects.filter(reg_no=reg_no).exists():
            obj.is_draft = False
            obj.save()
            return redirect('home')
        
        obj.save()
        arguement = reg_no
        url = reverse('add_student')+ '?'+get_url(arguement)
        return redirect(url)
    
    semesters = SemesterForm()
    session = SessionForm()
    context ={
        'semester':semesters,
        'session':session,
        'reg_no':student_reg,
    }
    return render(request,'add_record.html',context)


class AllRecordView(UserPassesTestMixin,ListView):
    model = Record
    template_name = 'all_record.html'
    success_url = ''
    context_object_name = 'records'
    def get_context_data(self, **kwargs: Any):
        context = super(AllRecordView,self).get_context_data(**kwargs)
        dept =Department.objects.all()
        context.update({'depts':dept})
        return context
    def post(self,*args, **kwargs):
        record_id = self.request.POST['delete']
        record = Record.objects.get(id = record_id)
        record.delete()
        return redirect('all_records')
    # def get_context_data(self,*args, **kwargs):
    #     context =super(AllRecordView,self).get_context_data(args,kwargs)
    #     records = Record.objects.filter(is_draft = False)
    #     context.update({'records':records})
    #     return context
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False 
    
def login(request):
    if request.method=="POST":
        username = request.POST['staffid']
        password = request.POST['passkeys']
        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return redirect('home')
            context={
                'error':'Your Account is suspended'
                    }
            return render(request,'login.html',context)
        context={
            'error':'Invalid StaffID or PassKeys'
        }
        return render(request,'login.html',context)
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'login.html')

class AllStudentsView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student_list.html'
    def test_func(self):
        if self.request.user.is_authenticated:
            return True
        return False  
class UpdateStudentsView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Student
    form_class = StudentForm
    context_object_name = 'students'
    template_name = 'update_students.html'
    success_url = '/all/students/'
    def test_func(self,*args,**kwargs):
        if self.request.user.is_superuser:
            return True
        return False 
    def post(self,*args,**kwargs):
        #print(self.request.POST)
        dept = Department.objects.get(name = self.request.POST['department'])
        reg_no = self.request.POST.get('reg_no')
        first_name =self.request.POST['first_name']
        middle_name =self.request.POST.get('middle_name')
        level = self.request.POST.get('level')
        last_name = self.request.POST.get('last_name')
        course_option = self.request.POST.get('course_option')
        student = Student.objects.get(reg_no = reg_no)
        student.first_name=first_name
        student.middle_name=middle_name
        student.level=int(level)
        student.last_name=last_name
        student.course_option=course_option
        student.department=dept
        student.save()
        return redirect('allstudents')
        # student = Student.objects.get(reg_no = self.request.POST['reg_no'])
        # student.department =  dept
        # student.save()
        # return redirect('allstudents')

        # return redirect('allstudents')
       

    
     
class AllUsersView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users.html'
    def test_func(self):
        if self.request.user.is_authenticated:
            return True
        return False   
    def post(self,*args, **kwargs):
        try:
            user_id = self.request.POST['delete']
            user = User.objects.get(username = user_id)
            user.delete()
            return redirect('users')
        except Exception:
            username = self.request.POST['staffid']
            password1 =self.request.POST['passkeys1']
            password2 =self.request.POST['passkeys2']
            first_name =self.request.POST['first_name']
            email =self.request.POST['email']
            errors = []
            if not self.request.user.is_superuser:
                errors.append('You are not granted this Priviladge of creating a Staff')
                context = {
                    'errors':errors
                }
                return render(self.request,'users.html',context)
            if User.objects.filter(username =username).exists():
                errors.append('StaffID already Exist')
            if not '@' in email.strip():
                errors.append('Email is not a valid mail')
            if password1.strip() != password2.strip():
                errors.append('The two passkeys are not the same')

            if errors:
                context = {
                    'errors':errors
                }
                return render(self.request,'users.html',context)
            obj = User(
                username = username,
                first_name = first_name,
                email = email,
            )
            obj.set_password(password1)
            obj.save()
            return redirect('users')



def add_student(request,*args,**kwargs):
    form = StudentForm()
    encoded_argument = request.GET.get('arg')
  
    if encoded_argument:
        argument = encoded_argument.replace('%2F', '/')
        context={
        'form':form,
        'reg':argument,
        'error':'No Student record with provided Reg.Number, please Add this student'

    }
        return render(request,'add_student.html',context)
    if request.method =="POST":
        reg_no = request.POST['reg_no']
        if Student.objects.filter(reg_no =reg_no).exists():
            context ={
                'error':'Registration Number Already Exist!',
                'form':form
            }
            return render(request,'add_student.html',context)
        form = StudentForm(request.POST)
        dept = Department.objects.get(name = request.POST.get('department'))
        if form.is_valid():
            form.save()
            student = Student.objects.get(reg_no =request.POST['reg_no'])
            student.department = dept
            student.save()
            records =Record.objects.filter(reg_no =request.POST['reg_no'])
            if records :
                for record in records:
                    record.is_draft = False
                    record.save()
            return redirect('allstudents')
        else:
            context ={
                'errors':form.errors,
                'form':form
            }
            return render(request,'add_student.html',context)
    context={
        'form':form
    }
    return render(request,'add_student.html',context)


class AddDepartment(UserPassesTestMixin,CreateView):
    model = Department
    template_name = 'add_dept.html'
    success_url = '/all/department/'
    fields = ['name']
    def get_context_data(self, **kwargs: Any):
        context = super(AddDepartment,self).get_context_data(**kwargs)
        dept =Department.objects.all()
        context.update({'depts':dept})
        return context
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False 
    
class AllDepartment(UserPassesTestMixin,ListView):
    model = Department
    template_name = 'all_dept.html'
    context_object_name = 'depts'
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False 


class DepartmentUpdateView(UserPassesTestMixin,UpdateView):
    template_name = 'update_dept.html'
    success_url = '/all/department/'
    fields =['name']
    model = Department
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
     
class SingleDepartment(UserPassesTestMixin,DetailView):
    model = Department
    template_name = 'department.html'
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False 


class StudentDetail(UserPassesTestMixin,DetailView):
    model = Student
    template_name = 'student_detail.html'
    def get_context_data(self,*args,**kwargs):
        pk= self.kwargs.get('pk')
        student = Student.objects.get(id =pk)
        context =  super(StudentDetail,self).get_context_data(*args,**kwargs)
        records = Record.objects.filter(reg_no =student.reg_no)
        context.update({'records':records})
        return context
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False 
    