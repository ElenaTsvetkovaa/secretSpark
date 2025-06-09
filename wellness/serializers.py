from rest_framework import serializers

from wellness.choices import MoodChoices
from wellness.models import Moods


class MoodsSerializer(serializers.ModelSerializer):
    is_default = serializers.SerializerMethodField()

    class Meta:
        model = Moods
        fields = '__all__'

    def get_is_default(self, obj):
        return obj.mood == MoodChoices.CALM



