from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Person, Participant
from .forms import PersonForm

# Create your views here.
def person_details_form(request):
    if request.method == "POST":
        # save data from request to form
        form = PersonForm(request.POST)
        if form.is_valid():
            Participant.objects.create(
                email=form.cleaned_data["email"],
                name=form.name(),
                preferences=form.preferences(),
            )
            return HttpResponseRedirect("thanks/")
    else:
        form = PersonForm()
    return render(request, "GAP/participant.html", {"form": form})


def person_view(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {"name": person.name, "email": person.email}
    return render(request, "GAP/user.html", context)


def participant_registration_success(request):
    return render(request, "GAP/participant_registration_success.html")
