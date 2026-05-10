from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

def analyze_aptamer(sequence):
    sequence = sequence.upper()
    length = len(sequence)
    gc_count = sequence.count('G') + sequence.count('C')
    gc_content = (gc_count / length) * 100 if length > 0 else 0
    binding_score = (gc_content * 0.4) + (length * 0.1)
    kd_value = round(100 / binding_score, 4) if binding_score > 0 else 0
    
    if kd_value < 1:
        sensitivity = "High"
        color = "green"
    elif kd_value < 10:
        sensitivity = "Medium"
        color = "orange"
    else:
        sensitivity = "Low"
        color = "red"
    
    return {
        "sequence": sequence,
        "length": length,
        "gc_content": round(gc_content, 2),
        "binding_score": round(binding_score, 2),
        "kd_value": kd_value,
        "sensitivity": sensitivity,
        "color": color
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    sequence = data.get('sequence', '')
    if not sequence:
        return jsonify({"error": "No sequence provided"}), 400
    result = analyze_aptamer(sequence)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
