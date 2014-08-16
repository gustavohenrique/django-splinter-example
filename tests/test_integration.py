from django.test import LiveServerTestCase
from django.test.utils import setup_test_environment
from django.db import connection
from django.conf import settings
from django.shortcuts import urlresolvers

from splinter import Browser
from splinter.request_handler.status_code import HttpResponseError

from poll.models import Candidate


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
        Candidate.objects.create(id=1, score=5)
        url = '%s%s' % (self.live_server_url, urlresolvers.reverse('vote', args='1'))
        self.browser.visit(url)
        self.assertEquals(self.browser.find_by_id('score1').first.text, u'100.00%')
        self.assertEquals(self.browser.find_by_id('score2').first.text, u'0.00%')

    def test_should_show_404_if_candidate_doesnt_exists(self):
        url = '%s%s' % (self.live_server_url, urlresolvers.reverse('vote', args='9'))
        self.assertRaises(HttpResponseError, self.browser.visit, url)
