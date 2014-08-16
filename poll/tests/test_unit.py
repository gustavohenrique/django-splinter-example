from django.test import TestCase, LiveServerTestCase

from poll.models import Poll
from poll import util


class UtilTest(TestCase):

    def test_calculate_percentual_scores_from_two_polls(self):
        p1 = Poll(id=1, score=6)
        p2 = Poll(id=2, score=4)
        result = util.calculate_scores(p1, p2)
        self.assertEquals(result.get('p1').get('id'), 1)
        self.assertEquals(result.get('p1').get('score'), '60.00')
        self.assertEquals(result.get('p2').get('id'), 2)
        self.assertEquals(result.get('p2').get('score'), '40.00')

    def test_should_return_percentual_zero_if_score_is_zero(self):
        p1 = Poll(id=1, score=0)
        p2 = Poll(id=2, score=0)
        result = util.calculate_scores(p1, p2)
        self.assertEquals(result.get('p1').get('id'), 1)
        self.assertEquals(result.get('p1').get('score'), '0.00')
        self.assertEquals(result.get('p2').get('id'), 2)
        self.assertEquals(result.get('p2').get('score'), '0.00')

    def test_should_return_empty_dict_when_args_is_none(self):
        result = util.calculate_scores(None, None)
        self.assertEquals(result, {})


class ViewTest(TestCase):

    def test_create_polls_if_database_is_empty(self):
        polls = Poll.objects.all()
        self.assertEquals(len(polls), 0)

        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        polls = Poll.objects.all()
        self.assertEquals(len(polls), 2)

    def test_increment_the_score_and_redirect_to_index(self):
        p = Poll.objects.create(score=6)

        response = self.client.get('/vote/%s/' % p.id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Poll.objects.get(pk=p.id).score, 7)

    def test_should_return_404_if_id_doesnt_exists(self):
        p = Poll.objects.create(score=6)

        response = self.client.get('/vote/99/')
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Poll.objects.get(pk=p.id).score, 6)


from django.test.utils import setup_test_environment
from django.db import connection
from django.conf import settings
from django.shortcuts import urlresolvers
from splinter import Browser
from splinter.request_handler.status_code import HttpResponseError


class IntegrationTest(LiveServerTestCase):

    def setUp(self):
        setup_test_environment()
        connection.creation.create_test_db(autoclobber=True)
        self.browser = Browser()

    def tearDown(self):
        connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])
        self.browser.quit()

    def test_show_index_page(self):
        url = '%s%s' % (self.live_server_url, urlresolvers.reverse('index'))
        self.browser.visit(url)
        self.assertEquals(self.browser.find_by_id('score1').first.text, u'0.00%')
        self.assertEquals(self.browser.find_by_id('score2').first.text, u'0.00%')

    def test_vote(self):
        Poll.objects.create(candidate_id=1, score=5)
        url = '%s%s' % (self.live_server_url, urlresolvers.reverse('vote', args='1'))
        self.browser.visit(url)
        self.assertEquals(self.browser.find_by_id('score1').first.text, u'100.00%')
        self.assertEquals(self.browser.find_by_id('score2').first.text, u'0.00%')

    def test_should_show_404_if_candidate_doesnt_exists(self):
        url = '%s%s' % (self.live_server_url, urlresolvers.reverse('vote', args='9'))
        self.assertRaises(HttpResponseError, self.browser.visit, url)

