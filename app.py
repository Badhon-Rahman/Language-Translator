from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_conversation():
    try:
        # Extract parameters from the request
        data = request.json
        conversation = data.get('conversation')
        conversation_current_language = data.get('conversationCurrentLanguage')
        expected_output_language = data.get('expectedOutputLanguage')

        # Validate input
        if not conversation or not conversation_current_language or not expected_output_language:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Translate conversation
        translated_text = translator.translate(
            conversation, 
            src=conversation_current_language, 
            dest=expected_output_language
        ).text

        # Return the translated text
        return jsonify({'translatedConversation': translated_text}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
