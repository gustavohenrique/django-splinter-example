# coding: utf-8

def calculate_scores(p1, p2):
    if p1 is None or p2 is None:
        return {}

    total = p1.score + p2.score
    score1 = _percentual(p1.score, total)
    score2 = _percentual(p2.score, total)

    return {
        'p1': {'id': p1.id, 'score': '{0:.2f}'.format(score1)},
        'p2': {'id': p2.id, 'score': '{0:.2f}'.format(score2)}
    }

def _percentual(score, total):
    try:
        return float(score) / float(total) * 100
    except ZeroDivisionError as e:
        return 0
