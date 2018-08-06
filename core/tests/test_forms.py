from django.test import TestCase

from core.forms import *
from testing_data import COMMENT_FORM_DATA


class FormsTestCase(TestCase):

    def test_valid_data(self):
        form = CommentForm(COMMENT_FORM_DATA)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = CommentForm({'content': '', 'rating': 0})
        self.assertFalse(form.is_valid())

    def test_comment_ratings_dict(self):
        self.assertTupleEqual(COMMENT_RATINGS[0], ('1', 1))
        self.assertTupleEqual(COMMENT_RATINGS[1], ('2', 2))
        self.assertTupleEqual(COMMENT_RATINGS[2], ('3', 3))
        self.assertTupleEqual(COMMENT_RATINGS[3], ('4', 4))
        self.assertTupleEqual(COMMENT_RATINGS[4], ('5', 5))
