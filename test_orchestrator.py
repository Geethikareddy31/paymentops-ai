import sys
import os

sys.path.append(os.path.abspath("src"))

from agent.orchestrator import process_incident


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


result = process_incident(incident)

print("\n==============================")
print("       PAYMENTOPS AI")
print("==============================")

print("\nDiagnosis:", result["diagnosis"])
print("Confidence:", round(result["confidence"] * 100, 2), "%")

print("\nAction:", result["decision"]["action"])
print("Reason:", result["decision"]["reason"])

print("\nResult:", result["result"]["status"])
print("Message:", result["result"]["message"])
print("Amount recovered: ₹", result["result"]["amount_recovered"])

print("\n--- AI Investigation ---")
print(result["explanation"])