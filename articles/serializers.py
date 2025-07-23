from rest_framework import serializers

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'title', 'category', 'updated_at', 'banner_url']

    def get_banner_url(self, obj):
        if obj.banner:
            return obj.banner_url
        return None







