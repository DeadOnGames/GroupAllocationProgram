from django.shortcuts import render, get_object_or_404
from .models import Person
from .forms import PersonForm

# Create your views here.
def person_details_form(request):
    if request.method == "POST":
        # save data from request to form
        form = PersonForm(request.post)
        if form.is_valid:
            return HttpResponseRedirect("/thanks/")
    else:
        form = PersonForm()
    return render(form, "GAP/participant.html", {"form": form})


def person_view(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {"name": person.name, "email": person.email}
    return render(request, "GAP/user.html", context)
