from django.shortcuts import render, get_object_or_404
from .models import Person

# Create your views here.
def person_view(request, person_id):
        person = get_object_or_404(Person, pk=person_id) 
        context = {"name":person.name, "email": person.email}
        return render(request, "GAP/user.html", context)
