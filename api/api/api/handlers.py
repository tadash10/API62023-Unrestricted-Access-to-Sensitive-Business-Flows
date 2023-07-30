from flask import request, jsonify
from flask_restful import Resource
from api.rate_limit import rate_limit_exceeded, update_request_count

def process_buy_ticket_request(api_key):
    # Process the buy ticket request
    # Add your buy ticket processing logic here
    return {'message': 'Ticket bought successfully'}

def process_post_comment_request(api_key):
    # Process the post comment request
    # Add your post comment processing logic here
    return {'message': 'Comment posted successfully'}

class BuyTicketResource(Resource):
    def post(self):
        # API endpoint to buy a ticket
        api_key = request.headers.get('API-Key')  # Assuming the API key is sent in the request header
        if not api_key:
            return handle_request_error('API key missing', 401)

        if rate_limit_exceeded(api_key, 'buy_ticket'):
            return handle_request_error('Rate limit exceeded', 429)

        # Process the buy ticket request
        response_data = process_buy_ticket_request(api_key)

        # Update the request count for the API key and endpoint
        update_request_count(api_key, 'buy_ticket')

        return jsonify(response_data)

class PostCommentResource(Resource):
    def post(self):
        # API endpoint to post a comment
        api_key = request.headers.get('API-Key')
        if not api_key:
            return handle_request_error('API key missing', 401)

        if rate_limit_exceeded(api_key, 'post_comment'):
            return handle_request_error('Rate limit exceeded', 429)

        # Process the post comment request
        response_data = process_post_comment_request(api_key)

        # Update the request count for the API key and endpoint
        update_request_count(api_key, 'post_comment')

        return jsonify(response_data)
