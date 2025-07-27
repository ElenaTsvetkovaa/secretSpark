from rest_framework import serializers
from diary.choices import MoodChoices
from diary.models import Moods, Diary


class MoodsSerializer(serializers.ModelSerializer):
    is_default = serializers.SerializerMethodField()

    class Meta:
        model = Moods
        fields = '__all__'

    def get_is_default(self, obj):
        return obj.mood == MoodChoices.CALM


class DiarySerializer(serializers.ModelSerializer):
    """
    mood -> Foreign key ID (write-only) - used when creating/updating
    mood_data -> serialized data of the mood object - provides mood name, image, reminder
    """
    mood_data = MoodsSerializer(source='mood', read_only=True)

    class Meta:
        model = Diary
        fields = ['id', 'date', 'content', 'mood', 'mood_data']
        extra_kwargs = {
            'mood': {'write_only': True}
        }

