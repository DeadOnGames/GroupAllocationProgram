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
                    Person.objects.create(name="test",email="test{0}@domain.com".format(i))
                    self.assertEqual(person_count+i+1,len(Person.objects.all()))
        def test_no_email_person(self):
                Person.objects.create(name="john smith")
                Person.objects.create(name="john stewart")
                self.assertEqual(len(Person.objects.all()),2)
                self.assertEqual(len(Person.objects.get(name="john smith")),1)
                self.assertEqual(len(Person.objects.get(name="john stewart")),1)
