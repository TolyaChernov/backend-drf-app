# from django.contrib.auth.models import User
from django.db import models

from users.models import CustomUser


class Collection(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Link(models.Model):
    WEBSITE = "website"
    BOOK = "book"
    ARTICLE = "article"
    MUSIC = "music"
    VIDEO = "video"
    LINK_TYPES = [
        (WEBSITE, "Website"),
        (BOOK, "Book"),
        (ARTICLE, "Article"),
        (MUSIC, "Music"),
        (VIDEO, "Video"),
    ]

    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    image = models.URLField(blank=True, null=True)
    link_type = models.CharField(
        max_length=20, choices=LINK_TYPES, default=WEBSITE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collections = models.ManyToManyField(Collection, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
