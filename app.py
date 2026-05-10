from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq
import json

app = Flask(__name__)
CORS(app)

def analyze_aptamer(sequence):
    seq = Seq(sequence.upper())
    gc_content = gc_fraction(seq) * 100
    length = len(seq)
    
    # Binding affinity prediction
    binding_score = (gc_content * 0.4) + (length * 0.1)
    kd_value = round(100 / binding_score, 4)
    
    # Biosensor threshold
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
    app.run(debug=True)