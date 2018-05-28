from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve
from ..views import boards_home, board_topics, new_topic

''' new imports below '''
from django.contrib.auth.models import User
from ..models import Board, Topic, Post
from ..forms import NewTopicForm

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('boards_home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)        #testing the status code of the response. The status code 200 means success.

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, boards_home)           #test if Django returned the correct view function for the requested URL

class BoardTopicsTests(TestCase):
    def setUp(self):                                        #setUp method, we prepare the environment to run the tests, so to simulate a scenario.
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):   #testing if Django is returning a status code 200 (success) for an existing Board.
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):  #testing if Django is using the correct view function to render the topics.
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('boards_home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('boards_home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('boards_home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, boards_home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))       #the assertContains method to test if the response body contains a given text.

class NewTopicTests(TestCase):
    def setUp(self):                    #creates a Board instance to be used during the tests
        Board.objects.create(name='Django', description='Django board.')

    def test_new_topic_view_success_status_code(self):                      #check if the request to the view is successful
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):                    #check if the view is raising a 404 error when the Board does not exist
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):                   #check if the right view is being used
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):  #ensure the navigation back to the list of topics
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):                                #make sure our HTML contains the token.
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):           #sends a valid combination of data and check if the view created a Topic instance and a Post instance.
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):         #ending an empty dictionary to check how the application is behaving.
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
