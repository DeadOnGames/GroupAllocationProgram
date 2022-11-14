from django.db import models

# Create your models here.
class Person(models.Model):
        name = models.CharField(max_length=50)
        email = models.EmailField(max_length=50)
        def __str__(self):
                return self.name
        #Override Save method
        def save(self, *args, **kwargs):
                if(self.email == "" or self.email == None):
                        super(Person, self).save(*args, **kwargs)
                        return
                try:
                        Person.objects.get(email = self.email)
                        raise Exception("Couldn't save person: Email Already Exists")
                except Person.DoesNotExist:
                        super(Person, self).save(*args, **kwargs)
