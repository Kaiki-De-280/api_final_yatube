from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        'Group', on_delete=models.SET_NULL, related_name='posts',
        null=True, blank=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Group(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=32)
    slug = models.SlugField(verbose_name='Слаг', max_length=32, unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Follow(models.Model):
    # Кто подписан
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follows'
    )
    # На кого подписан
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    class Meta:
        # Чтобы нельзя было подписаться дважды на одного и того же
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} -> {self.following.username}'
