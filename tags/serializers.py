from rest_framework import serializers
from .models import Tag
# from apps.newsletters.models import Newsletter
# from apps.newsletters.serializers import NewsletterSerializer


class TagSerializer(serializers.ModelSerializer):
    # newsletters = NewsletterSerializer(Newsletter, read_only=True,  many=True)
    class Meta:
        model = Tag
        fields = '__all__'