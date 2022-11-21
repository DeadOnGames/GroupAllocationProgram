from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name

    # define exception for invalid email
    class InvalidEmailException(Exception):
        message = "Email Invalid or Already Used"

    # Override Save method
    def save(self, *args, **kwargs):
        if self.email == "" or self.email == None:
            super(Person, self).save(*args, **kwargs)
            return
        try:
            Person.objects.get(email=self.email)
            raise Person.InvalidEmailException
        except Person.DoesNotExist:
            super(Person, self).save(*args, **kwargs)

class Group(models.Model):
    size = models.IntegerField(default=4)
    isApproved = models.BooleanField(default=False)
    task = models.CharField(max_length=50,null=True)

    def getScore(self):
        return False

    def getParticipants(self):
        return Participant.objects.get(group=self)

    def approve(self):
        self.isApproved = True

    def unapprove(self):
        self.isApproved = False

    def __str__(self):
        return f"Is the group approved?{self.isApproved}"


class SuperVisor_Model(Person):
    genderWeight = models.DecimalField(max_digits=11, decimal_places=10,default=1)
    preferenceWeight = models.DecimalField(max_digits=11, decimal_places=10,default=1)
    suggestedGroup = models.CharField(max_length=10,default="")
    def assignGroups(self):
        return False

    def approveGroups(self):
        return False

    def getGroups(self):
        return False

    def getParticipants(self):
        return False
class Participant(Person):
    preferences = models.ManyToManyField(Person, related_name="participant_preference",null=True)
    supervisor = models.ForeignKey(SuperVisor_Model, on_delete=models.CASCADE, related_name = "participant_supervisor",null=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE,null=True)

    def setPreferences(self, participant):
        self.preferences.add(participant)

    def getPreferences(self):
        return self.preferences.all()

    def assignGroup(self, group):
        self.group = group

    def setSupervisor(self, supervisor):
        self.supervisor = supervisor

    def removeFromGroup(self):
        self.group = None

    def getGroup(self):
        return self.group
