from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Person, Participant, Supervisor_Model
from .forms import PreferencesForm,ParticipantForm

# Create your views here.
def person_details_form(request, supervisor_id):
    message = ""
    if request.method == "POST":
        # save data from request to form
        form = ParticipantForm(request.POST)
        if form.is_valid():
            try:
                Participant.objects.create(
                    email=form.cleaned_data["email"],
                    name=form.name(),
                    supervisor = Supervisor_Model.objects.get(pk=supervisor_id)
                )
                return HttpResponseRedirect("thanks/")
            except Person.InvalidEmailException as e:
                message = e.message
    else:
        form = ParticipantForm()
    return render(request, "GAP/participant.html", {"form": form, "supervisor_id": supervisor_id, "error_message": message})
def participant_preference_form(request, participant_id):
    message = ""
    participant = Participant.objects.get(pk = participant_id)
    if request.method == "POST":
        # save data from request to form
        form = PreferencesForm(request.POST)
        if form.is_valid():
            participant.preferences = form.preferences()
            participant.save()
            message = "Choice Saved"
    else:
        form = PreferencesForm()
    return render(request, "GAP/preferences.html", {"form": form, "message": message, "name": participant.name, "participant_id": participant_id})

def person_view(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {"name": person.name, "email": person.email}
    return render(request, "GAP/user.html", context)
def register_supervisor(request):
    message=""
    if request.method == "POST":
        try:
            supervisor = Supervisor_Model.objects.create(name=request.POST["name"],email=request.POST["email"],group_size=request.POST["group_size"],gender_weight=request.POST["gender_weight"],preference_weight=request.POST["preference_weight"])
            message = "You've registered succesfully"
        except Exception as e:
            message = str(request.POST.keys()) + str(e)
    return render(request, "GAP/supervisor.html",{"weight_min": 0, "weight_max": 10, "message": message })



def participant_registration_success(request,supervisor_id):
    return render(request, "GAP/participant_registration_success.html")
