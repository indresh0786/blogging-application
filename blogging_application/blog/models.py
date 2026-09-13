from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=80,unique=True)
    def __str__(self): return self.name

class Post(models.Model):
    STATUS_CHOICES=[("draft","Draft"),("published","Published")]
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_posts")
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="posts")
    title=models.CharField(max_length=180)
    excerpt=models.CharField(max_length=260,blank=True)
    content=models.TextField()
    image_url=models.URLField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="draft")
    views=models.PositiveIntegerField(default=0)
    likes=models.ManyToManyField(User,blank=True,related_name="liked_posts")
    created_at=models.DateTimeField(default=timezone.now)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-created_at"]
    def __str__(self): return self.title
    def like_count(self): return self.likes.count()

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_comments")
    body=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=["-created_at"]
    def __str__(self): return f"{self.user.username} on {self.post.title}"
class PushSubscription(models.Model):
    endpoint = models.TextField(unique=True)
    p256dh = models.TextField()
    auth = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.endpoint[:50]