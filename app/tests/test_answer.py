import unittest
from .base import BaseTestCase
from ..models import Answer
from ..models import Question

answer = Answer()
question = Question()


class AnswersModelTestCase(BaseTestCase):

    def test_list_answers_without_token(self):
        '''Tests listing answers incorrectly
        e.g trying to list without JWT authorization header'''
        response = self.client.get(
            '/api/v1/questions/answers'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_answers_with_token(self):
        '''Tests listing answers correctly'''
        response = self.client.get(
            '/api/v1/questions/answers',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_post_answer(self):
        '''Tests updating an answer'''
        data = {
            'title': 'Test title',
            'body': 'Test body',
            'answer_body': 'Test answer',
            'user': self.user_id
        }

        """ Add test question."""
        self.client.post(
            '/api/v1/questions', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )

        response = self.client.get(
            '/api/v1/questions/',
            headers={'Authorization': 'JWT ' + self.token}
        )
        question_id = response.get_json().get('results')[0].get('question_id')

        """ Test posting an answer. """
        response = self.client.post(
            '/api/v1/questions/'+str(question_id)+'/answers', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )

        self.assertEqual(response.status_code, 201)

        """ Test if a question is created """
        self.assertEqual(response.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()