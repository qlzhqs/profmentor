import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Professions


class ProfessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professions
        fields = ("title", "slug", "content", "cat")











