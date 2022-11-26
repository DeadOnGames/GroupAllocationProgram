from django import forms
from .models import Participant


class PersonForm(forms.Form):
    def class_list():
        participants = []
        i = 1
        for p in Participant.objects.all():
            if p.email != "" and p.name != "":
                i += 1
                participants.append((i, p))
        return participants

    first_name = forms.CharField(label="First Name:", max_length=20)
    last_name = forms.CharField(max_length=20, label="Last Name:")
    wants_notified = forms.BooleanField(label="Notify Me when Groups Allocated:")
    email_address = forms.CharField(max_length=50, label="Email:")
    preferences = forms.ChoiceField(
        choices=class_list(), label="Who do you want to work with?"
    )
