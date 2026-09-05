import sys
import os

sys.path.append(os.path.abspath("src"))

from agent.orchestrator import process_incident


SCENARIOS = {

    "RISK DECLINE": {
        "transaction_id": "TEST-RISK-002",
        "amount": 8500,
        "method": "CARD",
        "issuer": "ICICI",
        "gateway_response_code": "DECLINED",
        "gateway_response_time_ms": 450,
        "retry_count": 0,
        "webhook_status": "failed",
        "webhook_attempts": 1,
        "recent_same_issuer_failures": 2,
        "recent_same_method_failures": 4,
        "failure_rate_last_5min": 0.08,
        "card_validity": "valid",
        "card_expiry_days": 240,
        "available_balance": 50000,
        "risk_score": 0.99,
        "customer_attempts_last_10min": 10
    },

    "INSUFFICIENT FUNDS": {
        "transaction_id": "TEST-FUNDS-003",
        "amount": 15000,
        "method": "CARD",
        "issuer": "SBI",
        "gateway_response_code": "DECLINED",
        "gateway_response_time_ms": 500,
        "retry_count": 0,
        "webhook_status": "failed",
        "webhook_attempts": 1,
        "recent_same_issuer_failures": 1,
        "recent_same_method_failures": 2,
        "failure_rate_last_5min": 0.05,
        "card_validity": "valid",
        "card_expiry_days": 400,
        "available_balance": 2000,
        "risk_score": 0.15,
        "customer_attempts_last_10min": 1
    },

    "RETRY LIMIT REACHED": {
        "transaction_id": "TEST-LIMIT-004",
        "amount": 10000,
        "method": "CARD",
        "issuer": "HDFC",
        "gateway_response_code": "TIMEOUT",
        "gateway_response_time_ms": 8000,
        "retry_count": 2,
        "webhook_status": "pending",
        "webhook_attempts": 3,
        "recent_same_issuer_failures": 10,
        "recent_same_method_failures": 30,
        "failure_rate_last_5min": 0.45,
        "card_validity": "valid",
        "card_expiry_days": 250,
        "available_balance": 50000,
        "risk_score": 0.20,
        "customer_attempts_last_10min": 2
    }
}


for name, incident in SCENARIOS.items():

    print("\n==============================")
    print(name)
    print("==============================")

    result = process_incident(incident)

    print("Diagnosis:", result["diagnosis"])
    print("Confidence:", round(result["confidence"] * 100, 2), "%")
    print("Action:", result["decision"]["action"])
    print("Result:", result["result"]["status"])
    print("Amount recovered: ₹", result["result"]["amount_recovered"])