# coding: utf-8
from django.shortcuts import render, redirect, urlresolvers, get_object_or_404

from poll.models import Poll
from poll import util


def index(request):
    p1 = Poll.objects.get_or_create(candidate_id=1)[0]
    p2 = Poll.objects.get_or_create(candidate_id=2)[0]
    result = util.calculate_scores(p1, p2)
    return render(request, 'index.html', result)

def vote(request, id):
    poll = get_object_or_404(Poll, candidate_id=id)
    poll.score += 1
    poll.save()
    return redirect(urlresolvers.reverse('index'))
