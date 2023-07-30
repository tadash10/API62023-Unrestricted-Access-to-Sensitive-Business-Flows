from flask import jsonify

def handle_request_error(error_message, status_code):
    # Helper function to handle common request errors
    response = jsonify({'error': error_message})
    response.status_code = status_code
    return response
