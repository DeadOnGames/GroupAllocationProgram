from django.test import TestCase
from .models import Person

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