from django.shortcuts import render
from .models import Person

# Create your views here.
def person_view(request, person_id):
        person = Person.objects.get(pk=person_id)
        context = {"name":person.name, "email": person.email}
        return render(request, "GAP/user.html",context)
