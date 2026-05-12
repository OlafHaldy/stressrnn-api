from flask import Flask, request, jsonify
from flask_cors import CORS
from stressrnn import StressRNN
import re

app = Flask(__name__)
CORS(app)

# Инициализация нейросети для расстановки ударений
stress_model = StressRNN()

def mark_stresses(text):
    """Расставляет ударения в тексте с помощью StressRNN"""
    try:
        result = stress_model.put_stress(text)
        return result
    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        return text

@app.route('/stress', methods=['POST'])
def handle_stress():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Текст не предоставлен'}), 400
    
    text = data['text']
    if not isinstance(text, str) or not text.strip():
        return jsonify({'error': 'Текст должен быть непустой строкой'}), 400
    
    try:
        stressed_text = mark_stresses(text)
        return jsonify({'result': stressed_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'API для расстановки ударений на основе StressRNN (нейросеть + словарь Зализняка)',
        'usage': 'POST /stress с телом {"text": "ваш текст"}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
