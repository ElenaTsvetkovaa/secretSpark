from datetime import date, datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from wellness.models import CycleCalendar
from wellness.views import CyclePhasesResultsView, calculate_phases, calculate_current_phase

UserModel = get_user_model()


class TestCycleResults(TestCase):

    def tearDown(self):
        CycleCalendar.objects.all().delete()
        UserModel.objects.all().delete()

    def setUp(self):
        user = UserModel.objects.create_user(
            username='Test',
            email='test@testing.com',
            password='fjdhfjdkfdk'
        )
        self.cycle_data = CycleCalendar.objects.create(
            profile=user.profile,
            last_period_date=date(2025, 7, 1),
            cycle_length=28,
            period_length=5
        )
        self.cycle_entries = {
            'last_period_date': date(2025, 7, 1),
            'cycle_length': 28,
            'period_length': 5
        }


    def test__CyclePhaseResults__with_logged_user__returns_phases(self):
        self.client.login(
            username='Test',
            password='fjdhfjdkfdk'
        )
        response =  self.client.get(reverse('api-show-results'))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('phases', response.data)
        self.assertIn('current_phase', response.data)

    def test__CyclePhaseResults__with_AnonymousUser__redirect_to_login(self):
        rf = RequestFactory()
        request = rf.get(reverse('api-show-results'))
        request.user = AnonymousUser()

        view_func = CyclePhasesResultsView.as_view()
        response = view_func(request)

        self.assertFalse(request.user.is_authenticated)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

