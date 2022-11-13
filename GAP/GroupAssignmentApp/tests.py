from django.test import TestCase
from .models import Person
from django.urls import reverse

# Create your tests here.
class PersonTests(TestCase):
        #tests string cast method
        def test_string_cast_returns_name(self):
                person = Person(name="Test Person")
                self.assertEqual("Test Person",str(person))
        #tests creation of person object
        def test_create_person(self):
                person_count = len(Person.objects.all())
                for i in range(0,10):
                    #Person.objects.create is auto generated constructor, saves instance to data base
                    Person.objects.create(name="test",email="test@domain.com")
                    self.assertEqual(person_count+i+1,len(Person.objects.all()))
#Test Person View
class PersonViewTests(TestCase):
        #Test 404 error returned if person view requested for does not exist
        def test_person_404(self):
                response = self.client.get(reverse("gaa:user",args=(1,)))
                self.assertEqual(response.status_code, 404)
        #Tests person view responds correctly if one Person created.
        def test_person_view(self):
                Person.objects.create(name = "test name",email="test@domain.com")
                response = self.client.get(reverse("gaa:user",args=(1,)))
                self.assertContains(response,"Name: test name")
                self.assertContains(response,"Email: test@domain.com")


