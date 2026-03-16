from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class PublisherManager(models.Manager):

    def get_queryset(self):
        return super(PublisherManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # chop etgan voxti
    created = models.DateTimeField(auto_now_add=True)  # yaratgan voxti hali chop etilmagan
    updated = models.DateTimeField(auto_now=True)  #  edit qilgan voxtini oladi.
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublisherManager()


    def get_absolute_url(self):
        return reverse("blogapp:post_detail", args=[self.publish.year,
                                                    self.publish.month,
                                                    self.publish.day,
                                                    self.slug])



posts = Post.objects.all()
p_posts = Post.published.all()




