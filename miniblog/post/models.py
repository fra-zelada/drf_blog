from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    asset_id = models.CharField(max_length=100)
    secure_url = models.URLField()

    def __str__(self):
        return f"Asset ID: {self.asset_id}"

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='posts_with_image', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.post.title}"
