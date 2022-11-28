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
    first_preference = forms.TypedChoiceField(
        choices=class_list(), label="First Preference:"
    )
    second_preference = forms.TypedChoiceField(
        choices=class_list(), label="Second Preference:"
    )
    third_preference = forms.TypedChoiceField(
        choices=class_list(), label="Third Preference:"
    )

    def preferences(self):
        if self.is_valid():
            p1 = self.cleaned_data["first_preference"]
            p2 = self.cleaned_data["second_preference"]
            p3 = self.cleaned_data["third_preference"]
            return "{},{},{}".format(p1, p2, p3)
        return

    def __init__(self, *args, **kw):
        super(PersonForm, self).__init__(*args, **kw)
        self.fields["first_preference"] = forms.TypedChoiceField(
            choices=PersonForm.class_list(), label="First Preference:"
        )
        self.fields["second_preference"] = forms.TypedChoiceField(
            choices=PersonForm.class_list(), label="Second Preference:"
        )
        self.fields["third_preference"] = forms.TypedChoiceField(
            choices=PersonForm.class_list(), label="Third Preference:"
        )
