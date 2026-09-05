import joblib
import pandas as pd

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from agent.decision_engine import decide_action
from agent.action_executor import execute_action
from agent.audit_logger import log_decision


# -----------------------------------------
# 1. Load the trained model
# -----------------------------------------

model = joblib.load(
    "models/diagnosis_model.joblib"
)


# -----------------------------------------
# 2. Create one payment incident
# -----------------------------------------

incident = {
    "transaction_id": "TXN-DEMO-001",
    "amount": 12000,
    "method": "CARD",
    "issuer": "HDFC",
    "gateway_response_code": "TIMEOUT",
    "gateway_response_time_ms": 7500,
    "retry_count": 1,
    "webhook_status": "pending",
    "webhook_attempts": 2,
    "recent_same_issuer_failures": 8,
    "recent_same_method_failures": 25,
    "failure_rate_last_5min": 0.35,
    "card_validity": "valid",
    "card_expiry_days": 300,
    "available_balance": 50000,
    "risk_score": 0.20,
    "customer_attempts_last_10min": 2
}


# -----------------------------------------
# 3. Convert incident into DataFrame
# -----------------------------------------

input_data = pd.DataFrame([incident])


# -----------------------------------------
# 4. Predict root cause
# -----------------------------------------

prediction = model.predict(input_data)[0]


# -----------------------------------------
# 5. Get probabilities
# -----------------------------------------

probabilities = model.predict_proba(input_data)[0]

classes = model.classes_


# -----------------------------------------
# 6. Get confidence
# -----------------------------------------

prediction_index = list(classes).index(
    prediction
)

confidence = probabilities[prediction_index]


# -----------------------------------------
# 7. Ask Decision Engine what to do
# -----------------------------------------

decision = decide_action(
    prediction,
    confidence,
    incident["retry_count"]
)

# -----------------------------------------
# 8. Execute approved action
# -----------------------------------------

result = execute_action(
    decision["action"],
    incident
)

# -----------------------------------------
# 9. Record decision in audit trail
# -----------------------------------------

audit_record = log_decision(
    incident,
    prediction,
    confidence,
    decision,
    result
)


# -----------------------------------------
# 10. Display complete result
# -----------------------------------------

print("\nPaymentOps AI")
print("======================")

print(
    "Diagnosis:",
    prediction
)

print(
    f"Confidence: {confidence * 100:.2f}%"
)

print(
    "Action:",
    decision["action"]
)

print(
    "Reason:",
    decision["reason"]
)

print(
    "Result:",
    result["status"]
)

print(
    "Message:",
    result["message"]
)

print(
    "Amount recovered: ₹",
    result["amount_recovered"]
)