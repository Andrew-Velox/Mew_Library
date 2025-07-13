from django.db import models

# Create your models here.


class BookCategory(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40,unique=True)

    def __str__(self):
        return f"{self.name}"