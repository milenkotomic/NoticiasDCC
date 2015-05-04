from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(max_length=100)
    view = models.CharField(max_length=400)
    view_prev = models.CharField(max_length=400)

    def __unicode__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=100)
    frequency = models.IntegerField(default=50)

    def __unicode__(self):
        return self.name


class Publication(models.Model):
    type_id = models.ForeignKey(Type)
    tag_id = models.ForeignKey(Tag)
    user_id = models.ForeignKey(User)
    template_id = models.ForeignKey(Template)
    priority_id = models.ForeignKey(Priority)
    init_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_user_id = models.ForeignKey(User, related_name="modification_user")
    modification_date = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    number = models.IntegerField()
    publication_id = models.ForeignKey(Publication)


class Text(models.Model):
    text = models.TextField()
    number = models.IntegerField()
    publication_id = models.ForeignKey(Publication)

    def __unicode__(self):
        return self.text