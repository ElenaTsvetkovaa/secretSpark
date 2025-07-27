from http import HTTPStatus
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from articles.models import Article, Section


class TestArticleCreation(TestCase):

    def tearDown(self):
        Article.objects.all().delete()
        Section.objects.all().delete()

    def setUp(self):
        self.post_data = {
            'title': 'Test Article',
            'category': 'style',

            'sections-TOTAL_FORMS': '2',
            'sections-INITIAL_FORMS': '0',
            'sections-MIN_NUM_FORMS': '0',
            'sections-MAX_NUM_FORMS': '1000',

            'sections-0-title': 'Section 1',
            'sections-0-content': 'Section 1 content',
            'sections-1-title': 'Section 2',
            'sections-1-content': 'Section 2 content'
        }

    @patch('cloudinary.models.CloudinaryField.pre_save')
    def test__form_valid__with_valid_article_data__expect_valid(self, mock_pre_save):
        mock_pre_save.return_value = 'mocked/image/path'

        def create_test_image(name='shared.jpg'):
            return SimpleUploadedFile(
                name=name,
                content=b'fake-image-data',
                content_type='image/jpeg'
            )

        file_data = {
            'banner': create_test_image('shared.jpg'),
            'sections-0-image': create_test_image('shared.jpg'),
            'sections-1-image': create_test_image('shared.jpg'),
        }
        url = reverse('create-article')
        response = self.client.post(url, data={**self.post_data, **file_data})

        success_url = reverse('article-category',  kwargs={'category': 'style'})
        
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Section.objects.count(), 2)
        self.assertRedirects(response, success_url, HTTPStatus.FOUND)
        
        article = Article.objects.first()
        self.assertNotEqual(article.banner, '')
        self.assertNotEqual(Section.objects.first().image, '')

    @patch('cloudinary.models.CloudinaryField.pre_save')
    def test__form_invalid__with_invalid_article_data__expect_invalid(self, mock_pre_save):
        mock_pre_save.return_value = 'mocked/image/path'

        def create_test_image(name='shared.jpg'):
            return SimpleUploadedFile(
                name=name,
                content=b'mock-image-data',
                content_type='image/jpeg'
            )

        file_data = {
            'banner': '',
            'sections-0-image': create_test_image('shared.jpg'),
            'sections-1-image': create_test_image('shared.jpg'),
        }
        
        self.post_data['title'] = ''
        url = reverse('create-article')
        response = self.client.post(url, data={**self.post_data, **file_data})
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'title', 'This field is required.')
        self.assertFormError(response.context['form'], 'banner', 'No file selected!')
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Section.objects.count(), 0)
