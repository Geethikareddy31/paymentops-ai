import joblib
import pandas as pd

from agent.decision_engine import decide_action
from agent.action_executor import execute_action
from agent.audit_logger import log_decision
from agent.investigation_agent import investigate


# -----------------------------------------
# Load trained model once
# -----------------------------------------

MODEL_PATH = "models/diagnosis_model.joblib"

model = joblib.load(MODEL_PATH)


def process_incident(incident):

    # -----------------------------------------
    # 1. Convert incident to DataFrame
    # -----------------------------------------

    input_data = pd.DataFrame([incident])


    # -----------------------------------------
    # 2. Diagnose incident
    # -----------------------------------------

    prediction = model.predict(
        input_data
    )[0]


    # -----------------------------------------
    # 3. Get confidence
    # -----------------------------------------

    probabilities = model.predict_proba(
        input_data
    )[0]

    classes = model.classes_

    prediction_index = list(classes).index(
        prediction
    )

    confidence = probabilities[
        prediction_index
    ]


    # -----------------------------------------
    # 4. Apply safety decision
    # -----------------------------------------

    decision = decide_action(
        prediction,
        confidence,
        incident["retry_count"]
    )


    # -----------------------------------------
    # 5. Execute approved action
    # -----------------------------------------

    result = execute_action(
        decision["action"],
        incident
    )


    # -----------------------------------------
    # 6. Record audit trail
    # -----------------------------------------

    log_decision(
        incident,
        prediction,
        confidence,
        decision,
        result
    )


    # -----------------------------------------
    # 7. Generate investigation explanation
    # -----------------------------------------

    explanation = investigate(
        incident,
        prediction,
        confidence,
        decision,
        result
    )


    # -----------------------------------------
    # 8. Return complete result
    # -----------------------------------------

    return {
        "diagnosis": prediction,
        "confidence": confidence,
        "decision": decision,
        "result": result,
        "explanation": explanation
    }