from rest_framework import serializers
from blog.models import Category, Tags, PostTags

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tags
		fields = '__all__'

class PostTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostTags
		fields = '__all__'