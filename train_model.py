
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Synthetic demonstration data
data = pd.DataFrame({
    "attendance_percentage": [
        95, 90, 88, 85, 82, 80, 78, 75, 72, 70,
        68, 65, 62, 60, 58, 55, 52, 50, 45, 40,
        98, 92, 86, 83, 79, 74, 69, 64, 57, 48
    ],
    "classes_missed": [
        1, 2, 3, 4, 5, 5, 6, 7, 8, 8,
        9, 10, 11, 12, 13, 14, 15, 16, 18, 20,
        0, 1, 3, 4, 6, 7, 9, 11, 14, 17
    ],
    "previous_score": [
        90, 85, 88, 82, 80, 78, 76, 75, 72, 70,
        68, 65, 63, 60, 58, 55, 52, 50, 45, 40,
        95, 91, 86, 84, 79, 74, 68, 64, 56, 48
    ],
    "at_risk": [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 1, 1, 1, 1
    ]
})

X = data[
    ["attendance_percentage", "classes_missed", "previous_score"]
]
y = data["at_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000, random_state=42)
)

mlflow.set_experiment("Student Attendance Risk Prediction")

with mlflow.start_run(run_name="attendance-logistic-regression"):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)

    mlflow.log_param("algorithm", "LogisticRegression")
    mlflow.log_param("test_size", 0.25)
    mlflow.log_param("random_state", 42)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)

    mlflow.sklearn.log_model(
        sk_model=model,
        name="attendance_model",
        input_example=X_train.head(3)
    )

    print(f"Accuracy:  {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print("Model and experiment details logged to MLflow.")

print("Training complete.")
