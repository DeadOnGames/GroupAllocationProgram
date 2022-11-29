from django import forms
from .models import Participant


class PersonForm(forms.Form):
    def class_list():
        participants = []
        i = 1
        try:
            part = Participant.objects.all()
            for p in part:
                if p.email != "" and p.name != "":
                    i += 1
                    participants.append((p.id, p))
            return participants
        except:
            return participants

    def name(self):
        return "{} {}".format(
            self.cleaned_data["first_name"], self.cleaned_data["last_name"]
        )

    first_name = forms.CharField(label="First Name:", max_length=20)
    last_name = forms.CharField(max_length=20, label="Last Name:")
    wants_notified = forms.BooleanField(label="Notify Me when Groups Allocated:")
    email = forms.CharField(max_length=50, label="Email:")
    n_preferences = 3

    def preferences(self):
        out = ""
        if self.is_valid():
            for i in range(1, self.n_preferences):
                out += "{},".format(self.cleaned_data["preference_{}".format(i)])
            out += str(self.cleaned_data["preference_{}".format(self.n_preferences)])
        return out

    def __init__(self, *args, n_preferences=3, **kw):
        self.n_preferences = n_preferences
        super(PersonForm, self).__init__(*args, **kw)
        for i in range(0, n_preferences):
            self.fields["preference_{}".format(i + 1)] = forms.TypedChoiceField(
                choices=PersonForm.class_list(), label="Preference: {}".format(i + 1)
            )
