from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Person, Participant, Supervisor_Model
from .forms import PersonForm

# Create your views here.
def person_details_form(request, supervisor_id):
    message = ""
    if request.method == "POST":
        # save data from request to form
        form = PersonForm(request.POST)
        if form.is_valid():
            try:
                Participant.objects.create(
                    email=form.cleaned_data["email"],
                    name=form.name(),
                    preferences=form.preferences(),
                    supervisor = Supervisor_Model.objects.get(pk=supervisor_id)
                )
                return HttpResponseRedirect("thanks/")
            except Person.InvalidEmailException as e:
                message = e.message
    else:
        form = PersonForm()
    return render(request, "GAP/participant.html", {"form": form, "supervisor_id": supervisor_id, "error_message": message})


def person_view(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {"name": person.name, "email": person.email}
    return render(request, "GAP/user.html", context)


def participant_registration_success(request,supervisor_id):
    return render(request, "GAP/participant_registration_success.html")
