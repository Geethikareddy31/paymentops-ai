import json
import os
from datetime import datetime


AUDIT_FILE = "data/audit_log.jsonl"


def log_decision(
    incident,
    diagnosis,
    confidence,
    decision,
    result
):

    # -----------------------------------------
    # Create audit record
    # -----------------------------------------

    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "transaction_id": incident.get("transaction_id", "DEMO"),
        "amount": incident["amount"],
        "diagnosis": diagnosis,
        "confidence": round(confidence, 4),
        "action": decision["action"],
        "reason": decision["reason"],
        "result": result["status"],
        "message": result["message"],
        "amount_recovered": result["amount_recovered"]
    }


    # -----------------------------------------
    # Make sure data directory exists
    # -----------------------------------------

    os.makedirs("data", exist_ok=True)


    # -----------------------------------------
    # Append record to audit log
    # -----------------------------------------

    with open(
        AUDIT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(audit_record)
            + "\n"
        )


    return audit_record