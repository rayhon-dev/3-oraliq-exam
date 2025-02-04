from django.db import models
from authors.base_model import BaseModel
from django.utils.text import slugify



class Catalog(BaseModel):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Catalog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(Catalog, self).save(*args, **kwargs)