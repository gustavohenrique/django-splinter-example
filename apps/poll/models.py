# coding: utf-8
from django.db import models

class Candidate(models.Model):
    score = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return '#%s = %s' % (self.id, self.score)

