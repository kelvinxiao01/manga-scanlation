from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from manga_ocr import MangaOcr
from PIL import Image
import io
import deepl

load_dotenv()
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

app = Flask(__name__)
CORS(app)

MANGA_OCR_URL = 'https://api.manga-ocr.com'
DEEPL_API_URL = 'https://api.deepl.com/v2/translate'

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']

        manga_text = extract_text(file)
        if manga_text is None:
            return jsonify({'error': 'Text extraction failed'}), 500

        translation = translate_text(manga_text)
        if translation is None:
            return jsonify({'error': 'Translation failed'}), 500

        return jsonify({'translation': translation})
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {str(e)}")
        # Return a generic error message
        return jsonify({'error': 'An internal server error occurred'}), 500
    
def extract_text(image):
    # Initialize the Manga OCR
    manga_ocr = MangaOcr()

    # Convert the byte stream to a PIL.Image object
    image.seek(0)  # Go to the beginning of the file
    image_bytes = image.read()
    image_pil = Image.open(io.BytesIO(image_bytes))

    # Perform OCR on the image
    try:
        extracted_text = manga_ocr(image_pil)
        return extracted_text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

def translate_text(text):
    # Initiliaze deepL
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang="EN-US")
    print(result.text)  
    return(result.text)

if __name__ == '__main__':
    app.run(debug=True)
