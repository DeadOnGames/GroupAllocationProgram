from django.db import models

# Create your models here.
class Person(models.Model):
        name = models.CharField(max_length=50)
        email = models.EmailField(max_length=50)
        def __str__(self):
                return self.name
        #define exception for invalid email
        class InvalidEmailException(Exception):
                message = "Email Invalid or Already Used"
        #Override Save method
        def save(self, *args, **kwargs):
                if(self.email == "" or self.email == None):
                        super(Person, self).save(*args, **kwargs)
                        return
                try:
                        Person.objects.get(email = self.email)
                        raise Person.InvalidEmailException
                except Person.DoesNotExist:
                        super(Person, self).save(*args, **kwargs)
