# api_key_validation.py
VALID_API_KEYS = ["your_valid_api_key_1", "your_valid_api_key_2"]  # Add valid API keys here

def is_valid_api_key(api_key):
    # Function to validate API keys against the list of valid keys
    return api_key in VALID_API_KEYS
