# coding: utf-8
from django.shortcuts import render, redirect, urlresolvers, get_object_or_404

from poll.models import Candidate
from poll import util


def index(request):
    c1 = Candidate.objects.get_or_create(id=1)[0]
    c2 = Candidate.objects.get_or_create(id=2)[0]
    result = util.calculate_scores(c1, c2)
    return render(request, 'index.html', result)

def vote(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.score += 1
    candidate.save()
    return redirect(urlresolvers.reverse('index'))
