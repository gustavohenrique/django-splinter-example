from django.test import TestCase

from poll.models import Candidate
from poll import util


class UtilTest(TestCase):

    def test_calculate_percentual_scores_from_two_candidates(self):
        c1 = Candidate(id=1, score=6)
        c2 = Candidate(id=2, score=4)
        result = util.calculate_scores(c1, c2)
        self.assertEquals(result.get('c1').get('id'), 1)
        self.assertEquals(result.get('c1').get('score'), '60.00')
        self.assertEquals(result.get('c2').get('id'), 2)
        self.assertEquals(result.get('c2').get('score'), '40.00')

    def test_should_return_percentual_zero_if_score_is_zero(self):
        c1 = Candidate(id=1, score=0)
        c2 = Candidate(id=2, score=0)
        result = util.calculate_scores(c1, c2)
        self.assertEquals(result.get('c1').get('id'), 1)
        self.assertEquals(result.get('c1').get('score'), '0.00')
        self.assertEquals(result.get('c2').get('id'), 2)
        self.assertEquals(result.get('c2').get('score'), '0.00')

    def test_should_return_empty_dict_when_args_is_none(self):
        result = util.calculate_scores(None, None)
        self.assertEquals(result, {})


class ViewTest(TestCase):

    def test_create_Candidates_if_database_is_empty(self):
        candidates = Candidate.objects.all()
        self.assertEquals(len(candidates), 0)

        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        candidates = Candidate.objects.all()
        self.assertEquals(len(candidates), 2)

    def test_increment_the_score_and_redirect_to_index(self):
        candidate = Candidate.objects.create(score=6)

        response = self.client.get('/vote/%s/' % candidate.id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Candidate.objects.get(pk=candidate.id).score, 7)

    def test_should_return_404_if_id_doesnt_exists(self):
        candidate = Candidate.objects.create(score=6)

        response = self.client.get('/vote/99/')
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Candidate.objects.get(pk=candidate.id).score, 6)
