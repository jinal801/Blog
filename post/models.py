from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel

from users.models import User


# Create your models here.
class Post(TimeStampedModel, ActivatorModel):
    """model for the post."""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    content = models.CharField(max_length=250)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return self.title


class Like(TimeStampedModel, ActivatorModel):
    """model for the like."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title