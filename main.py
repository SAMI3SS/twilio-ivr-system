import json
from flask import Flask, request, session
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Load postal codes from JSON file
try:
    with open(Config.POSTAL_CODES_FILE, 'r', encoding='utf-8') as file:
        postal_codes_data = json.load(file)
except FileNotFoundError:
    print(f"Warning: Postal codes file {Config.POSTAL_CODES_FILE} not found. Using empty list.")
    postal_codes_data = []

def extract_postal_code(text):
    """Extract numeric postal code from speech text"""
    numeric_text = ''.join(filter(str.isdigit, text))
    return numeric_text

def find_matching_postal_code(postal_code):
    """Find matching postal code in the database"""
    for entry in postal_codes_data:
        if entry.get('zipcode') == postal_code or entry.get('postal_code') == postal_code:
            return entry
    return None

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()

    if 'gather_attempts' not in session:
        session['gather_attempts'] = 0
        session['selected_postal_code'] = ''
        session['customer_type'] = ''

    if request.method == 'POST':
        speech_result = request.values.get('SpeechResult')
        print("User input:", speech_result)  # Debug info
        
        if speech_result:
            postal_code = extract_postal_code(speech_result)
            print("Detected postal code:", postal_code)  # Debug info

            if postal_code:
                matching_postal = find_matching_postal_code(postal_code)
                print("Matching postal code:", matching_postal)  # Debug info

                if matching_postal:
                    session['selected_postal_code'] = postal_code
                    confirmed_postal_code = session['selected_postal_code']
                    gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
                    # Ask user to confirm yes/no
                    gather.say(f'Did you say {confirmed_postal_code} as your postal code? Please confirm with "Yes" or "No".', language='en-US', voice='Polly.Joanna')
                    resp.append(gather)
                    session['gather_attempts'] += 1
                    print(confirmed_postal_code)
                    return str(resp)
                else:
                    gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
                    resp.say(f'Invalid postal code. Please provide your correct postal code.', language='en-US', voice='Polly.Joanna')                
                    resp.append(gather)
                    session['gather_attempts'] = 0
                    session['gather_attempts'] += 1
                    return str(resp)

            elif session['gather_attempts'] == 2:
                # Check yes or no response
                choice = speech_result.strip().lower()
                if choice in ['yes', 'yeah', 'yep', 'correct', 'right', 'sure', 'okay', 'ok', 'absolutely', 'indeed', 'exactly', 'precisely']:
                    gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
                    gather.say(f'Are you a private or business customer? Please say "private" or "business".', language='en-US', voice='Polly.Joanna')
                    resp.append(gather)
                    session['gather_attempts'] += 1
                    return str(resp)
            
                elif choice in ['no', 'nope', 'not', 'wrong', 'incorrect', 'false', 'negative', 'nah', 'never']:
                    gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
                    gather.say('Could you please tell me your postal code again?', language='en-US', voice='Polly.Joanna')
                    resp.append(gather)
                    session['gather_attempts'] = 0
                    session['gather_attempts'] += 1
                else:
                    gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
                    resp.say(f'I did not understand. If the postal code is correct, please say "yes". If the postal code is wrong, please say "no".', language='en-US', voice='Polly.Joanna')
                    resp.append(gather)
                    session['gather_attempts'] = 0  
                    session['gather_attempts'] += 2
                    return str(resp)

            elif session['gather_attempts'] == 3:
                # Get customer type information
                customer_type = speech_result.strip().lower()
                if customer_type in ['private', 'personal', 'individual', 'home', 'residential']:
                    correct_postal_code = session['selected_postal_code']
                    # Find data corresponding to the correct postal code
                    matching_postal = next((entry for entry in postal_codes_data if entry.get('zipcode') == correct_postal_code or entry.get('postal_code') == correct_postal_code), None)
                    if matching_postal:
                        resp.say(f'Thank you very much. You will now be connected to our customer service.', language='en-US', voice='Polly.Joanna')
                        resp.dial(Config.CUSTOMER_SERVICE_NUMBER)
                        from_number = request.values.get('From')
                        
                        # Log call information (you can customize this)
                        print(f"Call from: {from_number}")
                        print(f"Postal code: {correct_postal_code}")
                        print(f"Customer type: {customer_type}")
                        print(f"Full speech: {speech_result}")
                        
                        resp.hangup()
                        return str(resp)
                elif customer_type in ['business', 'commercial', 'corporate', 'company', 'enterprise', 'office']:
                    correct_postal_code = session['selected_postal_code']
                    matching_postal = next((entry for entry in postal_codes_data if entry.get('zipcode') == correct_postal_code or entry.get('postal_code') == correct_postal_code), None)
                    if matching_postal:
                        resp.say(f'Thank you very much. You will now be connected to our business services.', language='en-US', voice='Polly.Joanna')
                        resp.dial(Config.BUSINESS_SERVICE_NUMBER)
                        from_number = request.values.get('From')
                        
                        # Log call information
                        print(f"Business call from: {from_number}")
                        print(f"Postal code: {correct_postal_code}")
                        print(f"Customer type: {customer_type}")
                        print(f"Full speech: {speech_result}")
                        
                        resp.hangup()
                        return str(resp)
                else:
                    gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
                    gather.say('I did not understand. Could you please say "private" or "business" again?', language='en-US', voice='Polly.Joanna')
                    resp.append(gather)
                    session['gather_attempts'] = 0
                    session['gather_attempts'] += 3
                    return str(resp)

    if session['gather_attempts'] == 0:
        gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
        resp.say(Config.WELCOME_MESSAGE, language='en-US', voice='Polly.Joanna')
        resp.append(gather)
        session['gather_attempts'] += 1
        return str(resp)

    else:
        gather = Gather(input='speech', action='/voice', method='POST', timeout=4, language='en-US')
        resp.say(f'I did not understand you. Please tell me your postal code.', language='en-US', voice='Polly.Joanna')                
        resp.append(gather)
        session['gather_attempts'] = 0
        session['gather_attempts'] += 1
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
