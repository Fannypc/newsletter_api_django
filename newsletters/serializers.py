from rest_framework import serializers
from .models import Newsletter
from django.contrib.auth.models import User


# from apps.tags.models import Tag
# from apps.tags.serializers import TagSerializer


class NewsletterSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(Tag, many=True)
    class Meta:
        model = Newsletter
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class GuestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Newsletter_Guest
#         fields = '__all__'