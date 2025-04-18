from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
User = get_user_model()

from posts.models import Comment, Post, Group, Follow


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('post',)
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        # запрещаем подписываться на самого себя
        request_user = self.context['request'].user
        if value == request_user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value

    def validate(self, attrs):
        # дополнительно проверим уникальность подписки
        user = self.context['request'].user
        if Follow.objects.filter(user=user, following=attrs['following']).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        return attrs

    def create(self, validated_data):
        # сохраняем user автоматически
        return Follow.objects.create(
            user=self.context['request'].user,
            following=validated_data['following']
        )
