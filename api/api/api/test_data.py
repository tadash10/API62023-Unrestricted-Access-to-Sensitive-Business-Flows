# test_data.py
# Test data for unit tests

# Test API keys and secrets
TEST_API_KEY = "test_api_key"
TEST_SECRET = "test_secret"

# Test buy ticket request data
TEST_BUY_TICKET_REQUEST = {
    "name": "John Doe",
    "ticket_type": "standard",
    "quantity": 2
}

# Test post comment request data
TEST_POST_COMMENT_REQUEST = {
    "comment": "This is a test comment."
}

# Test response data for buy ticket and post comment endpoints
TEST_BUY_TICKET_RESPONSE = {
    "message": "Ticket bought successfully"
}

TEST_POST_COMMENT_RESPONSE = {
    "message": "Comment posted successfully"
}
