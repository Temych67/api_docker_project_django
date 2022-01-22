from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, unique=True)
    link = models.URLField(null=False, blank=False, unique=True)
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="date published"
    )
    amount_of_upvotes = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, null=False, blank=False)
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="date published"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "Comment to " + self.post.title + "; Author: " + self.author.username


class Vote(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
