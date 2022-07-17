from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Link(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    link = models.URLField(max_length=255, verbose_name="orign_url")
    user = models.ForeignKey(User, on_delete= models.SET_NULL, blank=True, null=True, verbose_name="user")


    def get_absolute_url(self):
        return reverse("", kwargs={"slug": self.slug})
    
    class Meta: 
        unique_together = ['user', 'link']
    

