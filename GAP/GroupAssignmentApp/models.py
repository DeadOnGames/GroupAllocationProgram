from django.db import models
import csv
from .HillClimb import hill_climb
from statistics import mean
from decimal import Decimal

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return "Name: {}, Email: {}".format(self.name, self.email)

    # define exception for invalid email
    class InvalidEmailException(Exception):
        message = "Email Invalid or Already Used"

    # Override Save method
    def save(self, *args, **kwargs):
        if self.email == "" or self.email == None:
            super(Person, self).save(*args, **kwargs)
            return
        try:
            if self.pk == Person.objects.get(email=self.email).pk:
                super(Person, self).save(*args, **kwargs)
            else:
                raise Person.InvalidEmailException
        except Person.DoesNotExist:
            super(Person, self).save(*args, **kwargs)


class Supervisor_Model(Person):
    group_size = models.IntegerField(default=2)
    gender_weight = models.DecimalField(max_digits=11, decimal_places=10, default=1)
    preference_weight = models.DecimalField(max_digits=11, decimal_places=10, default=1)
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
        return Decimal(self.gender_weight / s) * Decimal(
            s - abs(m_count - s / 2) - abs(f_count - (s / 2))
        )
    def score_allocation(self, allocation):
        return mean(map(self.score_group, allocation))

    def assign_groups(self):
        proposed_allocation =[]
        participants = Participant.objects.filter(supervisor=self)
        for i in range(0,len(participants)//self.group_size):
            group = []
            for j in range(0,self.group_size):
                group.append(participants[i*self.group_size + j])
            proposed_allocation.append(group)
        #Deal with remainder group
        size = len(participants) % self.group_size
        proposed_allocation.append(participants[len(participants)-size:len(participants)])
        #run hill climb
        proposed_allocation = hill_climb(proposed_allocation,self.score_allocation)
        #create allocation object
        Allocation.FromList(self, proposed_allocation)
        return self.score_allocation(proposed_allocation)



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
    def FromList(supervisor, allocation_list):
        allocation = Allocation.objects.create(supervisor = supervisor)
        for g in allocation_list:
            group = Group.objects.create(size = supervisor.group_size, allocation=allocation)
            for participant in g:
                participant.group.add(group)



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
    preferences = models.CharField(max_length=20, default="")
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

    def LoadCsv(supervisor):
        with open("GroupAssignmentApp/demo_participants.csv", newline="") as csvfile:
            participants = csv.reader(csvfile, delimiter=",", quotechar='"')
            next(participants, None)
            preferences = []
            for row in participants:
                p = Participant.objects.create(
                    supervisor=supervisor, name=row[0], email=row[1], gender=row[2]
                )
                preferences.append((p, "{},{},{}".format(row[3], row[4], row[5])))
            for p in preferences:
                p[0].preferences = p[1]
                p[0].save()
                print("{},{}".format(p[0], p[1]))
