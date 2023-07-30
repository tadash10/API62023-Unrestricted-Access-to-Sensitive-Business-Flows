from flask import Flask, request, jsonify, make_response
import redis
import time

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Constants for rate limiting
REQUEST_LIMIT = 100  # Number of requests allowed per time window
TIME_WINDOW = 60  # Time window in seconds

def rate_limit_exceeded(api_key, endpoint):
    # This function checks if the request limit has been exceeded for the given API key and endpoint
    key = f"{api_key}:{endpoint}"
    count = redis_client.get(key)
    return int(count) >= REQUEST_LIMIT if count else False

def update_request_count(api_key, endpoint):
    # This function updates the request count for the given API key and endpoint
    key = f"{api_key}:{endpoint}"
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, TIME_WINDOW)

@app.route('/buy_ticket', methods=['POST'])
def buy_ticket():
    # API endpoint to buy a ticket
    api_key = request.headers.get('API-Key')  # Assuming the API key is sent in the request header
    if not api_key:
        return make_response(jsonify({'error': 'API key missing'}), 401)

    if rate_limit_exceeded(api_key, 'buy_ticket'):
        return make_response(jsonify({'error': 'Rate limit exceeded'}), 429)

    # Process the buy ticket request
    # ...

    # Update the request count for the API key and endpoint
    update_request_count(api_key, 'buy_ticket')

    return jsonify({'message': 'Ticket bought successfully'})

@app.route('/post_comment', methods=['POST'])
def post_comment():
    # API endpoint to post a comment
    api_key = request.headers.get('API-Key')
    if not api_key:
        return make_response(jsonify({'error': 'API key missing'}), 401)

    if rate_limit_exceeded(api_key, 'post_comment'):
        return make_response(jsonify({'error': 'Rate limit exceeded'}), 429)

    # Process the post comment request
    # ...

    # Update the request count for the API key and endpoint
    update_request_count(api_key, 'post_comment')

    return jsonify({'message': 'Comment posted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
