from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):

    # Override the username field
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.'),
        validators=[],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

class Session(models.Model):
   
    session_name = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.session_name}"

class Semester(models.Model):
    session = models.ForeignKey(Session,on_delete = models.CASCADE)
    semester_name = models.CharField(max_length=15)
    semester_fees = models.FloatField(default = 0)

    def __str__(self):
        return f'{self.semester_name}|{self.session.session_name}'


class Student(models.Model):
    level = (
        (1,"100L"),
        (2,'200L'),
        (3,'300L'),
        (4,"400L"),
        (5,'500L'),
    )
    reg_no = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30,blank=True,null=True)    
    middle_name = models.CharField(max_length=30,blank=True,null=True)
    last_name = models.CharField(max_length=30,blank=True, null=True)
    course_option= models.CharField(max_length=50)
    department= models.CharField(max_length=50)
    level = models.IntegerField(choices=level,default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.reg_no
    

class Record(models.Model):
    semester= models.ForeignKey(Semester,on_delete=models.CASCADE)
    item = models.CharField(max_length=50)
    reg_no = models.CharField(max_length=15, null=True,blank=True)
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    ammount_due = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    reciept_no = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)
    def __str__(self):
        return self.item
    
