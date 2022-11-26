from django import forms


class PersonForm(forms.Form):
    first_name = forms.charField(label="first_name", max_length=20)
    last_name = forms.charField(max_length=20, label="last_name")
