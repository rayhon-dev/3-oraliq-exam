from django.db import models
from authors.base_model import BaseModel
from django.utils.text import slugify
from authors.models import Author
from catalogs.models import Catalog
from tags.models import Tag
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(BaseModel):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'



    title = models.CharField(max_length=100)
    category = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    short_content = models.TextField()
    long_content = models.TextField()
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='posts')
    image = models.ImageField(upload_to='post_images/')
    reading_period = models.CharField(max_length=100)
    publish = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(Post, self).save(*args, **kwargs)


    def get_detail_url(self):
        return reverse(
            'posts:detail',
            kwargs={
                'year': self.created_at.year,
                'month': self.created_at.month,
                'day': self.created_at.day,
                'slug': self.slug
            })

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return f'Comment for {self.post.title } by {self.name}'

    class Meta:
        ordering = ['-created_at']