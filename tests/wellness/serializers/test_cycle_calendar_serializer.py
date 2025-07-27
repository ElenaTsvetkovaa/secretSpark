from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from wellness.models import CycleCalendar
from wellness.serializers import CalendarDataSerializer

UserModel = get_user_model()


class CalendarDataSerializerTests(TestCase):

    def tearDown(self):
        CycleCalendar.objects.all().delete()
        UserModel.objects.all().delete()

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='test',
            email='test@example.com',
            password='testpass123'
        )
        self.data = {
            'last_period_date': date(2025, 1, 1),
            'cycle_length': 28,
            'period_length': 5
        }
        self.cycle_data = CycleCalendar.objects.create(
            profile=self.user.profile,
            **self.data
        )

    def test__serialization__return_correct_values(self):
        serializer = CalendarDataSerializer(instance=self.cycle_data)
        data = serializer.data

        self.assertEqual(data['profile'], self.user.profile.id)
        self.assertEqual(data['last_period_date'], '2025-01-01')
        self.assertEqual(data['cycle_length'], 28)
        self.assertEqual(data['period_length'], 5)

    def test__serialization__with_missing_required_fields__return_error(self):
        self.data['last_period_date'] = ''

        serializer = CalendarDataSerializer(data=self.data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('last_period_date', serializer.errors)

    def test__serialization__with_partial_update__should_succeed(self):
        update_data = {'cycle_length': 25}

        serializer = CalendarDataSerializer(
            instance=self.cycle_data,
            data=update_data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        updated_instance = serializer.save()

        self.assertEqual(updated_instance.cycle_length, 25)
        self.assertEqual(updated_instance.profile, self.user.profile)