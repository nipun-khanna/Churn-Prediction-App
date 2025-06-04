from flask import Flask, request, jsonify, render_template
import logging
import pickle
import pandas as pd
import os

# Logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load Model
model = None
try:
  model_file = os.path.join(os.path.dirname(__file__), "../models/churn_model.pkl")
  with open(model_file, "rb") as file:
    model = pickle.load(file)
  logging.info("Churn model loaded successfully")
except Exception as exc:
  logging.error(f"Error loading churn model: {exc}")


@app.route("/predict", methods=["POST"])
def predict_churn():
  if model == None:
    return jsonify({"error": "Churn Model could not be loaded."}), 500
  
  try:
    data = request.get_json(force=True)

    required_features = ["tenure", "monthly_charges", "contract_type"]
    for feature in required_features:
      if feature not in data or not isinstance(data[feature], (int, float)):
        return jsonify({"error": f"Missing or invalid data for feature: {feature}"}), 400

    input_df = pd.DataFrame([data], columns=required_features)
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0][1]

    result = {
        'churn_prediction': int(prediction),
        'churn_probability': float(prediction_proba)
    }
    logging.info(f"Prediction made: {result}")
    return jsonify(result)

  except Exception as exc:
    logging.error(f"Error during prediction: {exc}")
    return jsonify({"error": f"An internal error occurred: {str(exc)}"}), 500
  

@app.route('/')
def home():
  return render_template("index.html")

if __name__ == '__main__':
  app.run(debug=True)