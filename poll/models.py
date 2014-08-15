# coding: utf-8
from django.db import models

class Poll(models.Model):
    candidate_id = models.PositiveIntegerField(default=1)
    score = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return '#%s = %s' % (self.candidate_id, self.score)

