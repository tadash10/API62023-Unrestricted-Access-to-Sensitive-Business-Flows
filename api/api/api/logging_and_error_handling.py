# logging_and_error_handling.py
import logging

def setup_logging():
    # Function to set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        handlers=[
            logging.FileHandler('api.log'),
            logging.StreamHandler()
        ]
    )

def log_event(message, level=logging.INFO):
    # Function to log important events and errors
    logging.log(level, message)

def handle_error(message, status_code):
    # Function to handle errors gracefully and provide meaningful error messages to clients
    response = jsonify({'error': message})
    response.status_code = status_code
    return response
