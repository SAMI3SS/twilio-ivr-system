# Interactive Voice Response (IVR) System

A flexible and configurable IVR system built with Flask and Twilio that can be customized for any business. The system collects postal codes from callers and routes them to appropriate departments based on customer type.

## Features

- **Speech Recognition**: Uses Twilio's speech recognition to understand caller input
- **Postal Code Validation**: Validates postal codes against a configurable database
- **Customer Type Routing**: Routes calls to different departments based on customer type (private/business)
- **Multi-language Support**: Easily configurable for different languages
- **Configurable Messages**: All voice prompts can be customized
- **Error Handling**: Graceful handling of invalid inputs and retry logic

## Prerequisites

- Python 3.7+
- Twilio account with a phone number
- Publicly accessible server (for webhook endpoints)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd IVR
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-change-this-in-production
   POSTAL_CODES_FILE=SpeechIVR/zipcodes.ch.json
   WELCOME_MESSAGE=Welcome to our customer service...
   CUSTOMER_SERVICE_NUMBER=+1234567890
   BUSINESS_SERVICE_NUMBER=+1234567891
   TWILIO_ACCOUNT_SID=your-account-sid
   TWILIO_AUTH_TOKEN=your-auth-token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

4. **Configure postal codes**
   - Replace `SpeechIVR/zipcodes.ch.json` with your country's postal codes
   - Format: JSON array with objects containing `zipcode` or `postal_code` fields

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-change-this` |
| `POSTAL_CODES_FILE` | Path to postal codes JSON file | `SpeechIVR/zipcodes.ch.json` |
| `WELCOME_MESSAGE` | Initial greeting message | Welcome message |
| `CUSTOMER_SERVICE_NUMBER` | Phone number for private customers | `+1234567890` |
| `BUSINESS_SERVICE_NUMBER` | Phone number for business customers | `+1234567891` |
| `SPEECH_LANGUAGE` | Speech recognition language | `en-US` |
| `SPEECH_VOICE` | Text-to-speech voice | `Polly.Joanna` |
| `SPEECH_TIMEOUT` | Speech input timeout (seconds) | `4` |

### Postal Codes Format

Your postal codes file should be a JSON array with this structure:

```json
[
  {
    "zipcode": "8001",
    "city": "Zurich",
    "canton": "ZH"
  },
  {
    "zipcode": "8002",
    "city": "Zurich",
    "canton": "ZH"
  }
]
```

## Usage

1. **Start the server**
   ```bash
   python main.py
   ```

2. **Configure Twilio webhook**
   - Log into your Twilio console
   - Go to your phone number settings
   - Set the webhook URL for incoming calls to: `https://your-domain.com/voice`

3. **Test the system**
   - Call your Twilio phone number
   - Follow the voice prompts
   - Provide a postal code and customer type

## Customization

### Changing Language

To change the language, update these environment variables:

```env
SPEECH_LANGUAGE=de-DE  # For German
SPEECH_VOICE=Polly.Vicki  # German voice
```

### Customizing Messages

Edit the `WELCOME_MESSAGE` environment variable or modify the messages in `main.py`:

```python
resp.say('Your custom message here', language='en-US', voice='Polly.Joanna')
```

### Adding New Customer Types

To add more customer types, modify the customer type detection logic in `main.py`:

```python
elif customer_type in ['premium', 'vip', 'enterprise']:
    # Handle premium customers
    resp.dial(Config.PREMIUM_SERVICE_NUMBER)
```

## Deployment

### Using ngrok (for testing)
```bash
ngrok http 5000
```

### Production Deployment
- Deploy to a cloud provider (Heroku, AWS, DigitalOcean, etc.)
- Set up HTTPS (required by Twilio)
- Configure environment variables
- Set up a domain name

## Security Notes

- Change the default `SECRET_KEY` in production
- Use environment variables for sensitive data
- Never commit API keys to version control
- Use HTTPS in production

## Troubleshooting

### Common Issues

1. **Webhook not receiving calls**
   - Ensure your server is publicly accessible
   - Check that the webhook URL is correct in Twilio
   - Verify HTTPS is enabled

2. **Speech recognition not working**
   - Check the `SPEECH_LANGUAGE` setting
   - Ensure the language matches your voice prompts

3. **Postal codes not validating**
   - Verify the JSON format of your postal codes file
   - Check that the file path is correct

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the maintainers. 