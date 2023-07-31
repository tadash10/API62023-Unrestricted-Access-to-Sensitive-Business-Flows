from flask import Flask
from flask_restful import Api
from api.handlers import BuyTicketResource, PostCommentResource
from api.api_key_validation import is_valid_api_key
from api.request_auth import authenticate_request, check_permissions
from api.logging_and_error_handling import setup_logging, log_event, handle_error
from api.caching import cache_response
from api.response_formatting_and_versioning import format_response, api_versioning

app = Flask(__name__)
api = Api(app)

# Setting up logging configuration
setup_logging()

# API Key Validation Middleware
@app.before_request
def validate_api_key():
    api_key = request.headers.get('API-Key')
    if not api_key or not is_valid_api_key(api_key):
        log_event('Unauthorized API key access.', level=logging.WARNING)
        return handle_error('Unauthorized', 401)

# Request Authentication and Authorization Middleware
@app.before_request
def authenticate_and_authorize_request():
    api_key = request.headers.get('API-Key')
    secret = request.headers.get('Secret')

    if not api_key or not secret:
        log_event('Missing API key or secret in request headers.', level=logging.WARNING)
        return handle_error('Missing API key or secret', 401)

    if not authenticate_request(api_key, secret):
        log_event('Invalid API key or secret.', level=logging.WARNING)
        return handle_error('Unauthorized', 401)

    endpoint = request.endpoint
    if not check_permissions(api_key, endpoint):
        log_event('Unauthorized access to the endpoint.', level=logging.WARNING)
        return handle_error('Forbidden', 403)

# BuyTicketResource
class BuyTicketResource(Resource):
    @cache_response()
    @api_versioning
    def post(self):
        # Process the buy ticket request
        response_data = process_buy_ticket_request(api_key)

        return format_response(response_data)

# PostCommentResource
class PostCommentResource(Resource):
    @cache_response()
    @api_versioning
    def post(self):
        # Process the post comment request
        response_data = process_post_comment_request(api_key)

        return format_response(response_data)

# Adding API resources
api.add_resource(BuyTicketResource, '/buy_ticket')
api.add_resource(PostCommentResource, '/post_comment')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
