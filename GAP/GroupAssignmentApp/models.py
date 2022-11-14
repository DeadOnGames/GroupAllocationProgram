from django.db import models

# Create your models here.
class Person(models.Model):
        name = models.CharField(max_length=50)
        email = models.EmailField(max_length=50)
        def __str__(self):
                return self.name
            
class Group(models.Model):
    size = models.IntegerField(default = 4)
    isApproved = models.BooleanField(default=False)
    task = models.CharField(max_length=50)
    
    def getScore(self):
        return False
    
    def getParticipants(self):
        return False
    
    def approve(self):
        return False        
    
    def unapprove(self):
        return False
    
    def __str__(self):
        return f"Is the group approved?{self.isApproved}"
