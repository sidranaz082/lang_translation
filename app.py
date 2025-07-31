from flask import Flask ,jsonify, request ,render_template
from translate import Translator
import logging

app= Flask(__name__)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Supported languages (ISO 639-1 codes)
SUPPORTED_LANGUAGES = {
    'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb',
    'zh', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'fi', 'fr', 'fy', 'gl',
    'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig',
    'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'ku', 'ky', 'lo',
    'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my',
    'ne', 'no', 'ny', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd',
    'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tl',
    'tg', 'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy',
    'xh', 'yi', 'yo', 'zu'
}
def create_response(status, message, data=None):
       return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), status

@app.route('/')
def home():
    """Render the HTML translation form"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    app.logger.info("Received translation request")

    if not request.is_json:
        return create_response(400, "Request must be JSON")

    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language', 'en').lower()

    # Validate text
    if not text or not isinstance(text, str) or not text.strip():
        return create_response(400, "Text must be a non-empty string")

    # Validate language
    if target_language not in SUPPORTED_LANGUAGES:
        return create_response(
            400,
            f"Invalid language code. Supported codes: {sorted(SUPPORTED_LANGUAGES)}"
        )

    try:
        translator = Translator(to_lang=target_language)
        translated_text = translator.translate(text)

        result = {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language
        }

        app.logger.info("Translation successful")
        return create_response(200, "Translation successful", result)

    except Exception as e:
        app.logger.error(f"Translation failed: {e}")
        return create_response(500, f"Translation failed: {e}")

if __name__ == '__main__':
    app.run(debug=True)