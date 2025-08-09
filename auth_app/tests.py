from django.test import TestCase
from django.utils import timezone
import datetime

from .models import User
# Create your tests here.

class UserModelTest(TestCase):

    def test_is_user_eligible_by_age(self):
        time = timezone.now() - datetime.timedelta(days=4800)
        user = User(username="test_user", email="user@test.com", first_name="Jaques", last_name="Chiraque", birthdate=time, gender='m', profile='REGULAR')
        self.assertIs(user.is_eligible(), True)
