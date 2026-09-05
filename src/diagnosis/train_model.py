import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix


# -----------------------------------------
# 1. Load dataset
# -----------------------------------------

df = pd.read_csv("data/incidents.csv")

print("Dataset loaded:", len(df), "records")


# -----------------------------------------
# 2. Separate features and target
# -----------------------------------------

X = df.drop(columns=["true_label"])
y = df["true_label"]


# -----------------------------------------
# 3. Tell the model which columns are text
# -----------------------------------------

categorical_features = [
    "method",
    "issuer",
    "gateway_response_code",
    "webhook_status",
    "card_validity"
]


# -----------------------------------------
# 4. Tell the model which columns are numbers
# -----------------------------------------

numeric_features = [
    "amount",
    "gateway_response_time_ms",
    "retry_count",
    "webhook_attempts",
    "recent_same_issuer_failures",
    "recent_same_method_failures",
    "failure_rate_last_5min",
    "card_expiry_days",
    "available_balance",
    "risk_score",
    "customer_attempts_last_10min"
]


# -----------------------------------------
# 5. Convert text into numbers
# -----------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# -----------------------------------------
# 6. Create Random Forest
# -----------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# -----------------------------------------
# 7. Create complete ML pipeline
# -----------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# -----------------------------------------
# 8. Split into training and testing data
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------------------
# 9. Train
# -----------------------------------------

pipeline.fit(X_train, y_train)


# -----------------------------------------
# 10. Make predictions
# -----------------------------------------

y_pred = pipeline.predict(X_test)


# -----------------------------------------
# 11. Classification report
# -----------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# -----------------------------------------
# 12. Confusion matrix
# -----------------------------------------

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\nConfusion Matrix:")

print("Actual rows → Predicted columns\n")

print("Labels:")
print(labels)

print("\n", cm)


# -----------------------------------------
# 13. Feature importance
# -----------------------------------------

feature_names = (
    pipeline
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

importances = (
    pipeline
    .named_steps["model"]
    .feature_importances_
)

feature_importance = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print("\nTop 15 Features:")

print(
    feature_importance.head(15).to_string(
        index=False
    )
)

# -----------------------------------------
# 14. Save trained model
# -----------------------------------------

os.makedirs("models", exist_ok=True)

model_path = "models/diagnosis_model.joblib"

joblib.dump(pipeline, model_path)

print("\nModel saved to:", model_path)