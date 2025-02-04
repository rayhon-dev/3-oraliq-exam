from django.db import models
from .base_model import BaseModel
from django.utils.text import slugify


class Author(BaseModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='author_photos/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            while Author.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(Author, self).save(*args, **kwargs)