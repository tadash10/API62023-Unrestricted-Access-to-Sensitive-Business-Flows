from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import redis
import time
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Constants for rate limiting
REQUEST_LIMIT = 100  # Number of requests allowed per time window
TIME_WINDOW = 60  # Time window in seconds

class RateLimitResource(Resource):
    def get_key(self, api_key, endpoint):
        # Generate a unique key for rate limiting based on API key and endpoint
        return f"{api_key}:{endpoint}"

    def rate_limit_exceeded(self, api_key, endpoint):
        # This function checks if the request limit has been exceeded for the given API key and endpoint
        key = self.get_key(api_key, endpoint)
        count = redis_client.get(key)
        return int(count) >= REQUEST_LIMIT if count else False

    def update_request_count(self, api_key, endpoint):
        # This function updates the request count for the given API key and endpoint
        key = self.get_key(api_key, endpoint)
        count = redis_client.incr(key)
        if count == 1:
            # Set the expiration time based on ISO 8601 formatted timestamp
            expire_at = (datetime.utcnow() + timedelta(seconds=TIME_WINDOW)).isoformat()
            redis_client.setex(key, TIME_WINDOW, expire_at)

class BuyTicketResource(RateLimitResource):
    def post(self):
        # API endpoint to buy a ticket
        api_key = request.headers.get('API-Key')  # Assuming the API key is sent in the request header
        if not api_key:
            return jsonify({'error': 'API key missing'}), 401

        if self.rate_limit_exceeded(api_key, 'buy_ticket'):
            return jsonify({'error': 'Rate limit exceeded'}), 429

        # Process the buy ticket request
        # ...

        # Update the request count for the API key and endpoint
        self.update_request_count(api_key, 'buy_ticket')

        return jsonify({'message': 'Ticket bought successfully'})

class PostCommentResource(RateLimitResource):
    def post(self):
        # API endpoint to post a comment
        api_key = request.headers.get('API-Key')
        if not api_key:
            return jsonify({'error': 'API key missing'}), 401

        if self.rate_limit_exceeded(api_key, 'post_comment'):
            return jsonify({'error': 'Rate limit exceeded'}), 429

        # Process the post comment request
        # ...

        # Update the request count for the API key and endpoint
        self.update_request_count(api_key, 'post_comment')

        return jsonify({'message': 'Comment posted successfully'})

# Adding API resources
api.add_resource(BuyTicketResource, '/buy_ticket')
api.add_resource(PostCommentResource, '/post_comment')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
