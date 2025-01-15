from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

STATUS = {
    "To Do": "To Do",
    "In Progress": "In Progress",
    "In Review": "In Review",
    "Done": "Done"
}

PRIORITIES = {
        "Highest" : "P1",
        "High" : "P2",
        "Medium" : "P3",
        "Low" : "P4",
        "Lowest" : "P5",
    }
    
class Issue(models.Model):
    title = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=300)
    logged_time = models.FloatField(default=0)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS.items(),  default="To Do")
    priorities = models.CharField(max_length=20, choices= STATUS.items(), default="Low")
    asigned = models.ForeignKey('CustomUser', on_delete=models.DO_NOTHING, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}-{self.id}"
    
  
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    issues = models.ManyToManyField(Issue, blank=True)
    team = models.CharField(max_length=20, default="team A")
    
    def __str__(self):
        return self.username