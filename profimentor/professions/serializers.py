import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Professions

# class ProfessionsModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

class ProfessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professions
        fields = ("title", "slug", "content", "cat")











    # title = serializers.CharField(max_length=255)
    # slug = serializers.SlugField(max_length=255)
    # content = serializers.CharField()
    # cat_id = serializers.IntegerField()
    #
    # def create(self, validated_data):
    #     return Professions.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.slug = validated_data.get("slug", instance.slug)
    #     instance.content = validated_data.get("content", instance.content)
    #     instance.cat_id = validated_data.get("cat_id", instance.cat_id)
    #     instance.save()
    #     return instance



# def encode():
#     model = ProfessionsModel('Python Developer', 'Content: Python Developer')
#     model_sr = ProfessionsSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Python Developer","content":"Content: Python Developer"}')
#     data = JSONParser().parse(stream)
#     serializer = ProfessionsSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
#
