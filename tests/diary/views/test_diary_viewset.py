from datetime import date
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from diary.models import Moods, Diary
from diary.serializers import DiarySerializer
from diary.choices import MoodChoices


UserModel = get_user_model()

class TestDiaryViewSet(TestCase):

    def tearDown(self):
        Diary.objects.all().delete()
        UserModel.objects.all().delete()

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='test',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_login(user=self.user)

        self.mood = Moods.objects.get(
            mood=MoodChoices.HAPPY,
        )
        self.entry_data = {
            'date': date(2025, 1, 1),
            'content': 'Some text',
            'mood': self.mood
        }

        self.diary = Diary.objects.create(
            profile=self.user.profile,
            **self.entry_data
        )
        self.given_date = '2025-01-01'

    @patch('diary.models.Moods.image')
    def test__get_by_date__with_selected_date_and_existing_obj__return_existing_data(self, mock_image):
        mock_image.url = '/media/moods/happy.png'

        url = reverse('diary-get-by-date')
        response = self.client.get(url, {'date': self.given_date})

        serializer = DiarySerializer(instance=self.diary)

        self.assertTrue(response.data['exists'])
        self.assertEqual(response.data['data']['date'], self.given_date)
        self.assertEqual(response.data['data']['content'], serializer.data['content'])
        self.assertEqual(response.data['data']['mood_data'], serializer.data['mood_data'])

    def test__get_by_date__with_no_date_given__return_400(self):
        url = reverse('diary-get-by-date')
        response = self.client.get(url, {'date': ''})

        self.assertEqual(response.data['error'], 'Date parameter is required')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test__get_by_date__with_unauthenticated_user__return_403(self):
        self.client.logout()

        url = reverse('diary-get-by-date')
        response = self.client.get(url, {'date': self.given_date})
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test__get_by_date__with_non_existing_diary__return_exists_false(self):
        Diary.objects.get(date=self.given_date).delete()
        url = reverse('diary-get-by-date')

        response = self.client.get(url, {'date': self.given_date})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['exists'])
        self.assertNotIn('data', response.data)

