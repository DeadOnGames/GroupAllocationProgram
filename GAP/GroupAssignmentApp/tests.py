from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from .models import Person, Group, Supervisor_Model, Participant, Allocation
from .forms import PreferencesForm
from .GenerateNeighbour import generate_neighbours
from statistics import mode
from .HillClimb import hill_climb

# Create your tests here.
class PersonTests(TestCase):
    # Test that string cast method returns name of Person.
    def test_string_cast_returns_name_and_email(self):
        person = Person(name="Test Person", email="tp@domain.com")
        self.assertEqual("Name: Test Person, Email: tp@domain.com", str(person))

    # Test that creation of person object saves new person to the Data Base.
    def test_create_person(self):
        person_count = len(Person.objects.all())
        for i in range(0, 10):
            # Person.objects.create is auto generated constructor, saves instance to data base
            Person.objects.create(name="test", email="test{}@domain.com".format(i))
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

    # test assigning allocation to group
    def test_assign_allocation(self):
        g = Group.objects.create()
        a = Allocation.objects.create()
        g.allocation = a
        g.save()
        g1 = Group.objects.create()

        self.assertEqual(len(a.group_set.all()), 1)


class SupervisorTests(TestCase):
    def test_score_group(self):
        s = Supervisor_Model.objects.create(gender_weight=1)
        group_arr = [
            Participant.objects.create(gender="male"),
            Participant.objects.create(gender="male"),
            Participant.objects.create(gender="female"),
            Participant.objects.create(gender="female"),
        ]
        self.assertEqual(s.score_group(group_arr), 1)
        group_arr[0].gender = "female"
        self.assertEqual(s.score_group(group_arr), 0.5)
        group_arr[0].gender = "male"
        group_arr[3].gender = "male"
        self.assertEqual(s.score_group(group_arr), 0.5)
    def test_make_group_list(self):
        s = Supervisor_Model.objects.create(gender_weight=5, name="Super Visor", email = "sv@gmail.com")
        for i in range(0,5):
            Participant.objects.create(gender="male",name="jeff{}".format(i), supervisor = s)
        for i in range(0,5):
            Participant.objects.create(gender="female",name="jane{}".format(i), supervisor = s)
        for i in range(0,20):
            s.group_size = i+1
            group_list =s.make_group_list()
            self.assertFalse(group_list is None)
            self.assertFalse(len(group_list) == 0)
            for group in group_list:
                self.assertFalse(len(group) == 0)

    def test_assign_groups_gender_weight(self):
        s = Supervisor_Model.objects.create(gender_weight=5, name="Super Visor", email = "sv@gmail.com")
        for i in range(0,5):
            Participant.objects.create(gender="male",name="jeff{}".format(i), supervisor = s)
        for i in range(0,5):
            Participant.objects.create(gender="female",name="jane{}".format(i), supervisor = s)
        for i in range(0,20):
            s.group_size = i+1
            s.assign_groups()

class AllocationTests(TestCase):
    def test_create(self):
        s = Supervisor_Model.objects.create()
        a = Allocation.objects.create(supervisor=s)


class GenerateNeighboursTests(TestCase):
    # Test out for input array of length one is empty 3d array
    def test_one_array_input(self):
        test_arr = [[1, 2, 3]]
        nhbrs = generate_neighbours(test_arr)
        self.assertEqual(nhbrs, [test_arr])

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

    # Test correct output for 3 elements in two arrays given
    def test_with_3_element_2_array(self):
        test_arr = [[1, 2], [3]]
        expected_out = [[[3, 2], [1]], [[1, 3], [2]]]
        self.assertEquals(generate_neighbours(test_arr), expected_out)

    # Test correct output for two, two element arrays
    def test_2_2_element_arrays(self):
        test_arr = [[1, 2], [3, 4]]
        expected_out = [[[3, 2], [1, 4]], [[4, 2], [3, 1]]]
        self.assertEqual(expected_out, generate_neighbours(test_arr))

    # Test error message if wrong input shape
    def test_wrong_shape(self):
        self.assertEqual("Error: No groups submitted", generate_neighbours([]))


class HillClimbTest(TestCase):
    # Example Eval Function for testing
    def Eval(node):
        return mode(map(sum, node))

    # Make 2d array for testing purposes
    def gen_array(i):
        arr_out = []
        for n in range(0, i):
            arr_out.append([])
            for m in range(0, 10):
                arr_out[n].append(100 * n + m)
        return arr_out

    # Test output same format as input
    def test_out_same_format_as_input(self):
        arr = HillClimbTest.gen_array(10)
        arr_out = hill_climb(arr, HillClimbTest.Eval)
        self.assertEqual(len(arr_out), len(arr))
        for i in range(0, 10):
            self.assertEqual(len(arr[i]), len(arr_out[i]))

    # Ensure Hill climb output better than input
    def test_improvement_given(self):
        for i in range(3, 10):
            arr = HillClimbTest.gen_array(i)
            self.assertTrue(
                HillClimbTest.Eval(arr)
                <= HillClimbTest.Eval(
                    hill_climb(arr, HillClimbTest.Eval, max_iterations=1)
                )
            )


# Test PreferencesForm
class PreferencesFormTest(TestCase):
    def test_class_list_function(self):
        Participant.objects.create(name="Joe Blogs", email="jb@gmail.com")
        self.assertEquals(len(PreferencesForm.class_list()), 1)
        Participant.objects.create(name="Joe Blogs Senior")
        self.assertEquals(len(PreferencesForm.class_list()), 1)
        p = Participant.objects.create(name="James Bond", email="jb007@gmail.com")
        self.assertEquals(len(PreferencesForm.class_list()), 2)
        self.assertEquals(PreferencesForm.class_list()[1][0], p.id)

    def test_constructor_no_request(self):
        test_form = PreferencesForm(n_preferences=5)
        for i in range(0, 5):
            self.assertTrue("preference_{}".format(i + 1) in test_form.fields.keys())

    def test_pick_preferences(self):
        # make 6 example participant
        part = []
        for i in range(0, 6):
            part.append(
                Participant.objects.create(
                    name="test {}".format(i), email="test{}@example.co.uk".format(i)
                )
            )
        # select preferences in request
        request = HttpRequest()
        self.assertEqual(len(part), len(Participant.objects.all()))

        request.POST = {
            "preference_1": part[0].id,
            "preference_2": part[1].id,
            "preference_3": part[5].id,
            "first_name": "test",
            "email": "test0@exmaple.co.uk",
            "last_name": "0",
            "wants_notified": True,
        }
        form = PreferencesForm(request.POST)
        self.assertTrue(form.is_valid())
        # correct choice ids
        choices = [1, 2, 6]
        self.assertEquals(
            "{},{},{}".format(choices[0], choices[1], choices[2]), form.preferences()
        )
