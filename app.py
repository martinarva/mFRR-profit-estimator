from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

def process_csv(filepath):
    df = pd.read_csv(filepath)

    # Convert "Start" column to datetime to extract Year & Month
    df["Start"] = pd.to_datetime(df["Start"])
    df["Year-Month"] = df["Start"].dt.to_period("M")  # Grouping by Year-Month (e.g., 2025-03)

    results = {}  # Dictionary to store results for each month

    # Group data by Year-Month
    for period, group in df.groupby("Year-Month"):
        downTot, downComp, upTot, upComp = 0, 0, 0, 0

        for _, r in group.iterrows():
            dur = r.Duration
            dir = r.Direction
            power = r["Activated power"]
            frr = r["mFRR price"]
            nps = r["NPS price"]

            if dir == "DOWN":
                kWh = dur / 60 * power / 1000
                money = (nps - frr) * kWh * 0.8 / 1000
                downTot += kWh
                downComp += money

            if dir == "UP":
                kWh = dur / 60 * power / 1000
                upTot += kWh
                money = (frr - nps) * kWh * 0.8 / 1000
                upComp += money

        totalCompensation = downComp + upComp

        # Store results for each Year-Month
        results[str(period)] = {
            "Total down kWh": round(downTot, 2),
            "Total down compensation (€)": round(downComp, 2),
            "Total up kWh": round(upTot, 2),
            "Total up compensation (€)": round(upComp, 2),
            "Total compensation (€)": round(totalCompensation, 2)
        }

    return results

@app.route('/')
def upload_page():
    return render_template('index.html')

# Get the absolute path of the working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Ensure the uploads directory is created at startup
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file!"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)  # Ensure directory exists before saving

    result = process_csv(filepath)
    os.remove(filepath)  # Cleanup after processing

    return jsonify(result)
