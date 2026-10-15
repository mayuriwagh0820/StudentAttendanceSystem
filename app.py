
import mlflow
import mlflow.sklearn
import pandas as pd

from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

PREDICTIONS = Counter(
    "attendance_predictions_total",
    "Total attendance predictions"
)

PREDICTION_LATENCY = Histogram(
    "attendance_prediction_duration_seconds",
    "Prediction request processing time"
)

# Small synthetic training data for demonstration only
X = pd.DataFrame({
    "attendance_percentage": [95, 90, 85, 75, 65, 55, 45, 40],
    "classes_missed": [1, 2, 4, 7, 10, 14, 18, 20],
    "previous_score": [90, 85, 82, 75, 65, 55, 45, 40]
})
y = [0, 0, 0, 0, 1, 1, 1, 1]

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000, random_state=42)
)
model.fit(X, y)

@app.get("/")
def home():
    return jsonify({
        "service": "Student Attendance Prediction API",
        "status": "running",
        "note": "Uses synthetic demonstration data"
    })

@app.post("/predict")
def predict():
    with PREDICTION_LATENCY.time():
        body = request.get_json(silent=True) or {}

        try:
            values = {
                "attendance_percentage": float(
                    body["attendance_percentage"]
                ),
                "classes_missed": float(body["classes_missed"]),
                "previous_score": float(body["previous_score"])
            }
        except (KeyError, TypeError, ValueError):
            return jsonify({
                "error": "Provide attendance_percentage, "
                         "classes_missed, and previous_score as numbers"
            }), 400

        if not (
            0 <= values["attendance_percentage"] <= 100
            and values["classes_missed"] >= 0
            and 0 <= values["previous_score"] <= 100
        ):
            return jsonify({"error": "Input values are out of range"}), 400

        sample = pd.DataFrame([values])
        prediction = int(model.predict(sample)[0])
        probability = float(model.predict_proba(sample)[0][1])

        PREDICTIONS.inc()

        return jsonify({
            "predicted_at_risk": prediction,
            "risk_probability": round(probability, 4),
            "demo_model": True
        })

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
