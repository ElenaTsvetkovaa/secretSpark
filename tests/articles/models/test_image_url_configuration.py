from unittest.mock import patch, MagicMock
from django.test import TestCase
from articles.models import Article


class TestImageUrlConfiguration(TestCase):

    def tearDown(self):
        Article.objects.all().delete()

    @patch('articles.models.cloudinary_url')
    def test__banner_url__return_cloudinary_url(self, mock_cloudinary_url):
        mock_url = 'https://res.cloudinary.com/test/banner.jpg'
        mock_cloudinary_url.return_value = (mock_url, None)

        article = Article.objects.create(
            title='Test Article',
            category='style',
        )

        mock_banner = MagicMock()
        mock_banner.public_id = 'test_banner_public_id'
        article.banner = mock_banner

        self.assertEqual(article.banner_url, mock_url)
        mock_cloudinary_url.assert_called_once_with(mock_banner.public_id, secure=True)


