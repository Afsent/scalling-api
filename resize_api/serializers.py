from rest_framework import serializers

from .models import Picture


class PictureSerializer(serializers.HyperlinkedModelSerializer):
    picture = serializers.ImageField(max_length=None)

    class Meta:
        model = Picture
        fields = ('id', 'picture')
