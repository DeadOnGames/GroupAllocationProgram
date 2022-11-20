from django.test import TestCase
from django.urls import reverse
from .models import Person, Group, Supervisor
from .GenerateNeighbour import generate_neighbours


# Create your tests here.
class PersonTests(TestCase):
    # Test that string cast method returns name of Person.
    def test_string_cast_returns_name(self):
        person = Person(name="Test Person")
        self.assertEqual("Test Person", str(person))

    # Test that creation of person object saves new person to the Data Base.
    def test_create_person(self):
        person_count = len(Person.objects.all())
        for i in range(0, 10):
            # Person.objects.create is auto generated constructor, saves instance to data base
            Person.objects.create(name="test", email="test{0}@domain.com".format(i))
            self.assertEqual(person_count + i + 1, len(Person.objects.all()))

    # Test that it is possible to create a Person object, and save it to data base, even if person has no email address
    # Potential use-case is if someone is testing web-app but has not created account.
    def test_no_email_person(self):
        Person.objects.create(name="john smith")
        Person.objects.create(name="john stewart")
        self.assertEqual(len(Person.objects.all()), 2)

    # Test that if there is an attempt to save two Person objects, both with the same email to the data-base, that this fails and throws an exception.
    def test_attempt_save_two_people_same_email(self):
        p1 = Person(name="Joe Blogs", email="jblogs@domain.com")
        p2 = Person(name="Jane Blogs", email="jblogs@domain.com")
        p1.save()
        self.assertEqual(len(Person.objects.all()), 1)
        exceptionRaised = False
        try:
            p2.save()
        except Person.InvalidEmailException as e:
            self.assertEqual(e.message, Person.InvalidEmailException.message)
            exceptionRaised = True
        self.assertEqual(len(Person.objects.all()), 1)
        self.assertTrue(exceptionRaised)


# Test Person View
class PersonViewTests(TestCase):
    # Test 404 error returned if person view requested for does not exist
    def test_person_404(self):
        response = self.client.get(reverse("gaa:user", args=(1,)))
        self.assertEqual(response.status_code, 404)

    # Tests person view responds correctly if one Person created.
    def test_person_view(self):
        Person.objects.create(name="test name", email="test@domain.com")
        response = self.client.get(reverse("gaa:user", args=(1,)))
        self.assertContains(response, "Name: test name")
        self.assertContains(response, "Email: test@domain.com")


class GroupTests(TestCase):
    # tests if approve function correctly changes isApproved variable
    def test_approve(self):
        g = Group.objects.create()
        self.assertFalse(g.isApproved)
        g.approve()
        self.assertTrue(g.isApproved)

    # tests if unapprove function correctly changes isApproved variable
    def test_unapprove(self):
        g = Group.objects.create()
        g.approve()
        self.assertTrue(g.isApproved)
        g.unapprove()
        self.assertFalse(g.isApproved)


class GenerateNeighboursTests(TestCase):
    # Test out for input array of length one is empty 3d array
    def test_one_array_input(self):
        test_arr = [[1, 2, 3]]
        nhbrs = generate_neighbours(test_arr)
        self.assertEqual(nhbrs, [[[]]])

    # Test that Input is not included as neighbour
    def test_input_not_included(self):
        test_arr = [[1, 2], [3]]
        nhbrs = generate_neighbours(test_arr)
        self.assertFalse(test_arr in nhbrs)

    # Test no duplicate neighbours.
    def test_no_duplicates(self):
        test_arr = [[1, 2], [3, 4], [5, 6, 7], [8]]
        nhbrs = generate_neighbours(test_arr)
        found_nhbrs = []
        for n in nhbrs:
            self.assertFalse(n in found_nhbrs)
            found_nhbrs.append(n)
    #Test correct output for 3 elements in two arrays given
    def test_with_3_element_2_array(self):
        test_arr = [[1,2],[3]]
        expected_out = [[[3,2],[1]],[[1,3],[2]]]
        self.assertEquals(generate_neighbours(test_arr),expected_out)
