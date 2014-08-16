# coding: utf-8

def calculate_scores(c1, c2):
    if c1 is None or c2 is None:
        return {}

    total = c1.score + c2.score
    score1 = _percentual(c1.score, total)
    score2 = _percentual(c2.score, total)

    return {
        'c1': {'id': c1.id, 'score': '{0:.2f}'.format(score1)},
        'c2': {'id': c2.id, 'score': '{0:.2f}'.format(score2)}
    }

def _percentual(score, total):
    try:
        return float(score) / float(total) * 100
    except ZeroDivisionError as e:
        return 0
