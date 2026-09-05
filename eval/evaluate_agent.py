import sys
import os
import random

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

# -----------------------------------------
# Allow Python to find files inside src
# -----------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from agent.decision_engine import decide_action
from agent.action_executor import execute_action
from agent.audit_logger import log_decision


# -----------------------------------------
# 1. Load dataset and trained model
# -----------------------------------------

df = pd.read_csv("data/incidents.csv")

model = joblib.load(
    "models/diagnosis_model.joblib"
)

print("Dataset loaded:", len(df), "records")


# -----------------------------------------
# 2. Recreate the same held-out test set
# -----------------------------------------

X = df.drop(columns=["true_label"])
y = df["true_label"]

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------------------
# 3. Predict the held-out incidents
# -----------------------------------------

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)

classes = model.classes_


# -----------------------------------------
# 4. Evaluation counters
# -----------------------------------------

total_incidents = len(X_test)

correct_diagnoses = 0

automatic_actions = 0

human_reviews = 0

successful_recoveries = 0

retry_actions = 0

total_amount_recovered = 0

total_retry_amount = 0

unsafe_retries = 0


# -----------------------------------------
# 5. Make random simulation reproducible
# -----------------------------------------

random.seed(42)


# -----------------------------------------
# 6. Process every held-out incident
# -----------------------------------------

for index, (_, incident_row) in enumerate(
    X_test.iterrows()
):

    incident = incident_row.to_dict()

    true_label = y_test.loc[
        incident_row.name
    ]

    prediction = predictions[index]

    # -------------------------------------
    # Get confidence
    # -------------------------------------

    prediction_index = list(classes).index(
        prediction
    )

    confidence = probabilities[index][
        prediction_index
    ]


    # -------------------------------------
    # Check diagnosis correctness
    # -------------------------------------

    if prediction == true_label:

        correct_diagnoses += 1


    # -------------------------------------
    # Ask Decision Engine
    # -------------------------------------

    decision = decide_action(
        prediction,
        confidence,
        incident["retry_count"]
    )


    # -------------------------------------
    # Count decision categories
    # -------------------------------------

    if decision["action"] in [
        "RETRY_PAYMENT",
        "RETRY_WEBHOOK"
    ]:

        automatic_actions += 1

    else:

        human_reviews += 1


    # -------------------------------------
    # Execute approved action
    # -------------------------------------

    result = execute_action(
        decision["action"],
        incident
    )


    # -------------------------------------
    # Count payment retries
    # -------------------------------------

    if decision["action"] == "RETRY_PAYMENT":

        retry_actions += 1

        total_retry_amount += incident["amount"]


        # Check for unsafe retry

        if true_label not in [
            "NETWORK_TIMEOUT",
            "GATEWAY_ERROR"
        ]:

            unsafe_retries += 1


    # -------------------------------------
    # Count successful payment recovery
    # -------------------------------------

    if (
        decision["action"] == "RETRY_PAYMENT"
        and result["status"] == "SUCCESS"
    ):

        successful_recoveries += 1

        total_amount_recovered += (
            result["amount_recovered"]
        )


    # -------------------------------------
    # Write audit record
    # -------------------------------------

    log_decision(
        incident,
        prediction,
        confidence,
        decision,
        result
    )

# -----------------------------------------
# 7. Calculate metrics
# -----------------------------------------

diagnosis_accuracy = (
    correct_diagnoses / total_incidents
)

automatic_action_rate = (
    automatic_actions / total_incidents
)

human_review_rate = (
    human_reviews / total_incidents
)

if retry_actions > 0:

    recovery_success_rate = (
        successful_recoveries / retry_actions
    )

else:

    recovery_success_rate = 0


# -----------------------------------------
# 8. Display results
# -----------------------------------------

print("\n")
print("PaymentOps AI - Agent Evaluation")
print("================================")

print(
    "Held-out incidents:",
    total_incidents
)

print(
    "Correct diagnoses:",
    correct_diagnoses
)

print(
    f"Diagnosis accuracy: "
    f"{diagnosis_accuracy * 100:.2f}%"
)

print(
    "Automatic actions:",
    automatic_actions
)

print(
    f"Automatic action rate: "
    f"{automatic_action_rate * 100:.2f}%"
)

print(
    "Human reviews:",
    human_reviews
)

print(
    f"Human review rate: "
    f"{human_review_rate * 100:.2f}%"
)

print(
    "Payment retries:",
    retry_actions
)

print(
    "Successful recoveries:",
    successful_recoveries
)

print(
    f"Retry success rate: "
    f"{recovery_success_rate * 100:.2f}%"
)

print(
    "Total amount considered for retry: ₹",
    total_retry_amount
)

print(
    "Total simulated amount recovered: ₹",
    total_amount_recovered
)

print(
    "Unsafe automatic retries:",
    unsafe_retries
)