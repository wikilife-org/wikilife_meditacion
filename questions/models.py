from django.conf import settings
from django.db import models

class Person(models.Model):
    create_time = models.DateTimeField("created on", auto_now_add=True)
    source = models.CharField(max_length=200, null=True, blank=True)    
    
class Poll(models.Model):
    question = models.CharField(max_length=200)
    sequence = models.IntegerField()
    photo = models.ImageField(upload_to = 'poll/', null=True, blank=True)
    def __unicode__(self):
        return self.question
    
    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return ""
            
    def has_photo(self):
        if self.photo:
            return True
        else:
            return False

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    photo = models.ImageField(upload_to = 'choice/', null=True, blank=True)

    def __unicode__(self):
        return self.choice

    def has_photo(self):
        if self.photo:
            return True
        else:
            return False

class Response(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)
    person = models.ForeignKey(Person)
    create_time = models.DateTimeField("created on", auto_now_add=True)


class Chart(models.Model):
    title = models.CharField(max_length=200)
    poll1 = models.ForeignKey(Poll, related_name="chart_poll1")
    poll2 = models.ForeignKey(Poll, related_name="chart_poll2")
    published = models.BooleanField()
    create_time = models.DateTimeField("created on", auto_now_add=True)
