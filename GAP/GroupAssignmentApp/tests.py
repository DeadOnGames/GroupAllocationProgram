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
        def test_attempt_save_two_people_same_email(self):
                p1 = Person(name = "Joe Blogs", email = "jblogs@domain.com")
                p2 = Person(name = "Jane Blogs", email = "jblogs@domain.com")
                p1.save()
                self.assertEqual(len(Person.objects.all()),1)
                exceptionRaised = False
                try:
                        p2.save()
                except Exception  as e:
                        self.assertEqual(str(e), "Couldn't save person: Email Already Exists")
                        exceptionRaised = True
                self.assertEqual(len(Person.objects.all()),1)
                self.assertTrue(exceptionRaised)
