from rest_framework import serializers

from movies.models import Filmwork


class NameListField(serializers.ListField):
    """Поле для списка значений."""

    name = serializers.CharField(read_only=True)


class FilmworkSerializer(serializers.ModelSerializer):
    """Сериализатор модели `Film`."""

    genres = NameListField(read_only=True)
    actors = NameListField(read_only=True)
    directors = NameListField(read_only=True)
    writers = NameListField(read_only=True)

    class Meta:
        model = Filmwork
        fields = (
            'id',
            'access_type',
            'title',
            'description',
            'release_date',
            'rating',
            'age_rating',
            'type',
            'genres',
            'actors',
            'directors',
            'writers',
        )
