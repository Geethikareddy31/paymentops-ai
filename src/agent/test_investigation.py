from investigation_agent import investigate


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


diagnosis = "NETWORK_TIMEOUT"

confidence = 0.895

decision = {
    "action": "RETRY_PAYMENT",
    "reason": "High-confidence network timeout is potentially transient."
}

result = {
    "status": "SUCCESS",
    "message": "Payment retry succeeded.",
    "amount_recovered": 12000
}


explanation = investigate(
    incident,
    diagnosis,
    confidence,
    decision,
    result
)


print("\nPaymentOps AI Investigation")
print("===========================")
print(explanation)