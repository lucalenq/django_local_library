from django.test import TestCase

import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question, Chart

from django.urls import reverse

import os

from django.conf import settings

from .my_classes import DataTool

# Create your tests here.

# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)

# class QuestionModelTests(TestCase):

#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)

#     def test_was_published_recently_with_old_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is older than 1 day.
#         """
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         old_question = Question(pub_date=time)
#         self.assertIs(old_question.was_published_recently(), False)

#     def test_was_published_recently_with_recent_question(self):
#         """
#         was_published_recently() returns True for questions whose pub_date
#         is within the last day.
#         """
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_question = Question(pub_date=time)
#         self.assertIs(recent_question.was_published_recently(), True)

#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )

    
#     class QuestionDetailViewTests(TestCase):
#         def test_future_question(self):
#             """
#             The detail view of a question with a pub_date in the future
#             returns a 404 not found.
#             """
#             future_question = create_question(question_text='Future question.', days=5)
#             url = reverse('polls:detail', args=(future_question.id,))
#             response = self.client.get(url)
#             self.assertEqual(response.status_code, 404)

#         def test_past_question(self):
#             """
#             The detail view of a question with a pub_date in the past
#             displays the question's text.
#             """
#             past_question = create_question(question_text='Past Question.', days=-5)
#             url = reverse('polls:detail', args=(past_question.id,))
#             response = self.client.get(url)
#             self.assertContains(response, past_question.question_text)
    
class HomeTests(TestCase):
    def test_one_dataframe_produce_facets(self):
        """
        Test if a single csv file becomes a dataframe then it generates facets.
        """

        fileName = ['df_idealista_bcn_pg_1_to_50.csv']
        
        # self.assertIsNot(output,'')       
        # output = Chart.displayFacets(os.path.join(  settings.STATICFILES_DIRS[0], 
        #                                             fileName
        #                                         )
        #                             )
        output = Chart.displayFacets(fileName)
        self.assertIsNot(output,'')

    def test_multiple_dataframes_produce_facets(self):
        """
        Test if multiple csv files become a dataframe then it generates facets.
        """

        lstfileNames = ['df_idealista_bcn_pg_1_to_50.csv',
                        'df_idealista_bcn_pg_51_to_100.csv',]
        
       
        # output = Chart.displayFacet(os.path.join(  settings.STATICFILES_DIRS[0], 
        #                                             lstfileNames
        #                                         )
        #                             )

        output = Chart.displayFacets(lstfileNames)
        self.assertIsNot(output,'')       
 
class DeployTests(TestCase):

    def test_if_procfile_is_ok_for_heroku(self):
        """
        The Procfile doesn't tell Heroku to run a web site for the application data_science_idealista.
        """
        test = False
        procfile = open('Procfile','r')
        if 'web: gunicorn data_science_idealista.wsgi --log-file -' in procfile.read():
            test = True
        procfile.close()
        self.assertIs(test,True)