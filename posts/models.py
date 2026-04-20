from django.db import models


class Post(models.Model):
    CATEGORY_NEWS = 'news'
    CATEGORY_POLITICS = 'politics'
    CATEGORY_SPORT = 'sport'
    CATEGORY_TECH = 'tech'
    CATEGORY_CULTURE = 'culture'

    CATEGORY_CHOICES = [
        (CATEGORY_NEWS, 'Новости'),
        (CATEGORY_POLITICS, 'Политика'),
        (CATEGORY_SPORT, 'Спорт'),
        (CATEGORY_TECH, 'Технологии'),
        (CATEGORY_CULTURE, 'Культура'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_NEWS,
    )

    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    video_thumbnail = models.ImageField(
        upload_to='posts/video_thumbnails/',
        blank=True,
        null=True,
    )

    views_count = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()
