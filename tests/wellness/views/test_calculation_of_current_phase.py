from datetime import date
from unittest.mock import patch

from django.test import TestCase

from wellness.models import CyclePhase
from wellness.views import calculate_current_phase_and_plans


class TestCurrentPhaseExtraction(TestCase):

    def setUp(self):
        self.original_phases = list(CyclePhase.objects.all())
        self.last_period = date(2025, 1, 1)
    
    def tearDown(self):
        CyclePhase.objects.all().delete()
        for phase in self.original_phases:
            CyclePhase.objects.create(name=phase.name, description=phase.description)

    @patch('wellness.views.datetime')
    def test__calculate_current_phase__return_follicular_phase(self, mock_date):
        mock_date.today.return_value.date.return_value = date(2025, 1, 14)

        result = calculate_current_phase_and_plans(
              last_period_date=self.last_period,
              period_length=5,
              cycle_length=28
        )
        expected_phase = 'follicular'
        self.assertEqual(result['name'].lower(), expected_phase)


    @patch('wellness.views.datetime')
    def test__calculate_current_phase__after_full_cycle_passed__return_menstrual(self, mock_date):
        mock_date.today.return_value.date.return_value = date(2025, 1,29)

        result = calculate_current_phase_and_plans(
              last_period_date=self.last_period,
              period_length=5,
              cycle_length=28
        )
        expected_phase = 'menstrual'
        self.assertEqual(result['name'].lower(), expected_phase)

    @patch('wellness.views.datetime')
    def test__calculate_current_phase__with_no__db_data__return_fallback_message(self, mock_date):
        CyclePhase.objects.all().delete()
        mock_date.today.return_value.date.return_value = date(2025, 1, 1)

        result = calculate_current_phase_and_plans(
              last_period_date=self.last_period,
              period_length=5,
              cycle_length=28
        )
        fallback = 'unknown'
        self.assertEqual(result['name'].lower(), fallback)

