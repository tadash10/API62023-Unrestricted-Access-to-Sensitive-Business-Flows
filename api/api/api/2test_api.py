
# test_api.py
import unittest
from unittest.mock import patch
from api.app import app
from api.test_data import (
    TEST_API_KEY, TEST_SECRET, TEST_BUY_TICKET_REQUEST,
    TEST_POST_COMMENT_REQUEST, TEST_BUY_TICKET_RESPONSE,
    TEST_POST_COMMENT_RESPONSE,
)

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # Test buy ticket endpoint
    @patch('api.handlers.process_buy_ticket_request')
    def test_buy_ticket_endpoint(self, mock_process_buy_ticket):
        mock_process_buy_ticket.return_value = TEST_BUY_TICKET_RESPONSE
        headers = {'API-Key': TEST_API_KEY, 'Secret': TEST_SECRET}
        response = self.app.post('/buy_ticket', json=TEST_BUY_TICKET_REQUEST, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, TEST_BUY_TICKET_RESPONSE)

    # Test post comment endpoint
    @patch('api.handlers.process_post_comment_request')
    def test_post_comment_endpoint(self, mock_process_post_comment):
        mock_process_post_comment.return_value = TEST_POST_COMMENT_RESPONSE
        headers = {'API-Key': TEST_API_KEY, 'Secret': TEST_SECRET}
        response = self.app.post('/post_comment', json=TEST_POST_COMMENT_REQUEST, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, TEST_POST_COMMENT_RESPONSE)

if __name__ == '__main__':
    unittest.main()
