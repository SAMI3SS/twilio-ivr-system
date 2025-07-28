import os

class Config:
    """Configuration settings for the IVR system"""
    
    # Flask secret key (change this in production)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
    
    # Postal codes file path
    POSTAL_CODES_FILE = os.environ.get('POSTAL_CODES_FILE', 'SpeechIVR/zipcodes.ch.json')
    
    # Welcome message (customize this for your business)
    WELCOME_MESSAGE = os.environ.get('WELCOME_MESSAGE', 
        'Welcome to our customer service. You are next in line. Please provide your postal code, and we will assist you immediately.')
    
    # Phone numbers to connect customers to
    CUSTOMER_SERVICE_NUMBER = os.environ.get('CUSTOMER_SERVICE_NUMBER', '+1234567890')
    BUSINESS_SERVICE_NUMBER = os.environ.get('BUSINESS_SERVICE_NUMBER', '+1234567891')
    
    # Twilio configuration (set these as environment variables)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'your-account-sid')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'your-auth-token')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+1234567890')
    
    # Speech recognition settings
    SPEECH_LANGUAGE = os.environ.get('SPEECH_LANGUAGE', 'en-US')
    SPEECH_VOICE = os.environ.get('SPEECH_VOICE', 'Polly.Joanna')
    SPEECH_TIMEOUT = int(os.environ.get('SPEECH_TIMEOUT', '4'))
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '5000'))
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true' 