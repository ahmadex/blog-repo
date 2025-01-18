from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BlogUser(models.Model):
    "BlogUser that stores user info as OneToOne related field and a role field."
    class UserRole(models.TextChoices):
        AUTHOR = "Author"
        READER = "Reader"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.READER)


class BlogPost(models.Model):
    "BlogPost that stores post information."

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(BlogUser, null=True, blank=True, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    "Comment that stores all the comments by user to the post."

    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class Reaction(models.Model):
    """Stores the reaction of the user for the posts"""
    class ReactionChoices(models.TextChoices):
        LIKE = "like"
        DISLIKE = "dislike"

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.CharField(max_length=10, choices=ReactionChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.reaction} - {self.post.title}"


class PostStatistics(models.Model):
    """Stores posts statastics data on daily basis"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    comments = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('post', 'date')
    
    def __str__(self):
        return f"{self.post.title} - {self.date}"