from django.test import TestCase
from .models import Student

# Create your tests here.
class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(name="Patrick", des = "Patrick is the best", owner = 1)

    def test_student_correct_owner(self):
        pat = Student.objects.get(name='Patrick')
        self.assertEqual(pat.name, 'Patrick')