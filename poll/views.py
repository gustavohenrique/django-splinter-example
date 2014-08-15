from django.shortcuts import render, redirect, urlresolvers, get_object_or_404

from poll.models import Poll


def index(request):
    p1 = Poll.objects.get_or_create(candidate_id=1)[0]
    p2 = Poll.objects.get_or_create(candidate_id=2)[0]
    total = p1.score + p2.score
    try:
        score1 = float(p1.score) / float(total) * 100
    except ZeroDivisionError as e:
        score1 = 0
    try:
        score2 = float(p2.score) / float(total) * 100
    except ZeroDivisionError as e:
        score2 = 0
    result = {
        'p1': {'id': p1.id, 'score': '{0:.2f}'.format(score1)},
        'p2': {'id': p2.id, 'score': '{0:.2f}'.format(score2)}
    }
    return render(request, 'index.html', result)


def vote(request, id):
    poll = get_object_or_404(Poll, candidate_id=id)
    poll.score += 1
    poll.save()
    return redirect(urlresolvers.reverse('index'))

