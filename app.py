from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

def process_csv(filepath):
    df = pd.read_csv(filepath)

    downTot, downComp, upTot, upComp = 0, 0, 0, 0

    for _, r in df.iterrows():
        dur = r.Duration
        dir = r.Direction
        power = r['Activated power']
        frr = r['mFRR price']
        nps = r['NPS price']

        if dir == 'DOWN':
            kWh = dur / 60 * power / 1000
            money = (nps - frr) * kWh * 0.8 / 1000
            downTot += kWh
            downComp += money

        if dir == 'UP':
            kWh = dur / 60 * power / 1000
            upTot += kWh
            money = (frr - nps) * kWh * 0.8 / 1000
            upComp += money

    totalCompensation = downComp + upComp  # New calculation
    
    return {
        "Total down kWh": round(downTot, 2),
        "Total down compensation (€)": round(downComp, 2),
        "Total up kWh": round(upTot, 2),
        "Total up compensation (€)": round(upComp, 2),
        "Total compensation (€)": round(totalCompensation, 2)
    }

@app.route('/')
def upload_page():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file!"}), 400

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    result = process_csv(filepath)
    os.remove(filepath)  # Cleanup

    return jsonify(result)

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
