from rest_framework import serializers

from account.models import User
from .models import Post

# class UserSerializer(serializers.Serializer):
#     full_name = serializers.CharField(max_length=100)
#     phone = serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=100)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', 'is_active', 'is_admin', 'last_login']


# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=100)
#     body = serializers.CharField()
#     is_published = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Article.objects.create(title=validated_data['title'], body=validated_data['body'])


def check_article(data):
    if len(data['body']) < 20:
        raise serializers.ValidationError('The body is too short')


class CheckArticle:
    def __call__(self, data):
        if len(data['body']) < 20:
            raise serializers.ValidationError('The body is too short')

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user','title', 'body']
        validators = [check_article]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Article.objects.create(**validated_data)