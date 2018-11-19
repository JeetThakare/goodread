from django.db import models
from django.urls import reverse

# Create your models here.


class Link(models.Model):
    url = models.CharField(max_length=256, unique=True)
    visited = models.BooleanField(default=False)
    article_fetched = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        indexes = [
            models.Index(fields=['url', 'visited']),
            models.Index(fields=['visited'], name='visited_idx'),
        ]

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse("Link_detail", kwargs={"pk": self.pk})


class Topic(models.Model):
    topic = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    # def __str__(self):
    #     return self.name

    def get_absolute_url(self):
        return reverse("Topic_detail", kwargs={"pk": self.pk})


class Article(models.Model):
    article = models.TextField()
    # topics = models.ForeignKey(
    #     Topic, on_delete=models.PROTECT, blank=True, null=True)
    url = models.CharField(max_length=256, unique=True)
    # title = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse("Article_detail", kwargs={"pk": self.pk})
