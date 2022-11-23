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


class Supervisor_Model(Person):
    genderWeight = models.DecimalField(max_digits=11, decimal_places=10, default=1)
    preferenceWeight = models.DecimalField(max_digits=11, decimal_places=10, default=1)
    suggestedGroup = models.CharField(max_length=10, default="")

    # First go at score group function, currently only works for gender distribution
    def score_group(self, group_list):
        m_count = 0
        f_count = 0
        s = len(group_list)
        for p in group_list:
            if p.gender == "male":
                m_count += 1
            else:
                f_count += 1
        return (self.genderWeight / s) * (
            s - abs(m_count - s / 2) - abs(f_count - (s / 2))
        )

    def assignGroups(self):
        return False

    def approveGroups(self):
        return False

    def getGroups(self):
        return False

    def getParticipants(self):
        return False


# An allocation will represent how people are split into groups.
# An allocation will be a foreign key of a group. Representing a group being in an allocation
# A supervisor will be a foreign key of an allocation. Representing "ownership" of the supervisor over the allocation
class Allocation(models.Model):
    supervisor = models.ForeignKey(
        Supervisor_Model,
        null=True,
        related_name="allocation_owner",
        on_delete=models.CASCADE,
    )


class Group(models.Model):
    size = models.IntegerField(default=4)
    isApproved = models.BooleanField(default=False)
    task = models.CharField(max_length=50, null=True)
    allocation = models.ForeignKey(Allocation, null=True, on_delete=models.CASCADE)

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


class Participant(Person):
    preferences = models.ManyToManyField(
        Person, related_name="participant_preference", null=True
    )
    supervisor = models.ForeignKey(
        Supervisor_Model,
        on_delete=models.CASCADE,
        related_name="participant_supervisor",
        null=True,
    )
    gender = models.CharField(max_length=8, default="male")
    # many to many field as each person will be in multiple groups.
    group = models.ManyToManyField(Group)

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
