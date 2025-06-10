from flask import Flask, request, jsonify, render_template
import logging
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
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

    required_features = ["tenure", "TotalCharges", "MonthlyCharges", "Contract_Month-to-month", "Contract_One year", "Contract_Two year"]
    for feature in required_features:
      if feature not in data:
        return jsonify({"error": f"Missing or invalid data for feature: {feature}"}), 400

    input_df = pd.DataFrame([data], columns=required_features)
    df = transform_data(input_df)
    
    prediction = model.predict(df)[0]
    prediction_proba = model.predict_proba(df)[0][1]

    result = {
        'churn_prediction': int(prediction),
        'churn_probability': float(prediction_proba)
    }
    logging.info(f"Prediction made: {result}")
    return jsonify(result)

  except Exception as exc:
    logging.error(f"Error during prediction: {exc}")
    return jsonify({"error": f"An internal error occurred: {str(exc)}"}), 500


def transform_data(df):
  features = ["tenure","MonthlyCharges","TotalCharges"]
  df_numerical = pd.DataFrame(df, columns=features)
  df_base = df.drop(columns=features)

  scaler = MinMaxScaler()
  transformed_numerical = scaler.fit_transform(df_numerical)
  scaled_df = pd.DataFrame(transformed_numerical, columns=features, index=df_base.index)

  return pd.concat([scaled_df, df_base], axis=1)

@app.route('/')
def home():
  return render_template("index.html")


if __name__ == '__main__':
  app.run(debug=True)