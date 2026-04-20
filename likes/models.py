from django.db import models
from posts.models import Post


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    ip_address = models.GenericIPAddressField()
    visitor_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'visitor_id'],
                name='unique_like_per_visitor_per_post',
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        owner = self.visitor_id or self.ip_address
        return f"Лайк {self.post.title} от {owner}"
