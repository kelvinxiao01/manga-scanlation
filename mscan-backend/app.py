from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

print("Here is the auth key:")
print(DEEPL_AUTH_KEY)

app = Flask(__name__)

MANGA_OCR_URL = 'https://api.manga-ocr.com'
DEEPL_API_URL = 'https://api.deepl.com/v2/translate'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    # Send file to Manga OCR
    manga_text = extract_text(file)
    if manga_text is None:
        return jsonify({'error': 'Text extraction failed'}), 500

    # Translate text with DeepL
    translation = translate_text(manga_text)
    if translation is None:
        return jsonify({'error': 'Translation failed'}), 500

    return jsonify({'translation': translation})

def extract_text(image):
    # Implement communication with Manga OCR here
    # ...
    return

def translate_text(text):
    # Implement communication with DeepL API here
    data = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': text,
        'target_lang': 'EN'  # Assuming translation to English
    }
    response = requests.post(DEEPL_API_URL, data=data)
    if response.status_code != 200:
        return None
    return response.json()['translations'][0]['text']

if __name__ == '__main__':
    app.run(debug=True)
