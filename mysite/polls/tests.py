import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
	"""
		creates a question with the given 'question_text' and publish the given number of 'days' offset to now
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)
	

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		"""
		if now question exists
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])
	
	def test_index_view_with_a_past_question(self):
		"""
		questions with a pub_date in the past should be displayed on the index page.
		"""
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
		response.context['latest_question_list'],
		['<Question: Past question.>']
		)

	def test_index_view_with_a_future_question(self):
		"""
			questions with pub_date in the future should not be displayed on the index page
		"""
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.asssertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])
		
	def test_index_view_with_future_question_and_past_question(self):
		"""
			even if both past and future questions exist, only past questions should be displayed.
		"""
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)
	
	def test_index_view_with_two past_questions(self):
		"""
			the question index page may display multiple questions.
		"""
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question 2.>','<Question: Past question 1.>']
		)
		
		
class QuestionIndexDetailTests(TestCase):
	