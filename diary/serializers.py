from rest_framework import serializers
from diary.choices import MoodChoices
from diary.models import Moods
from django.templatetags.static import static


class MoodsSerializer(serializers.ModelSerializer):
    is_default = serializers.SerializerMethodField()

    class Meta:
        model = Moods
        fields = '__all__'

    def get_is_default(self, obj):
        return obj.mood == MoodChoices.CALM


