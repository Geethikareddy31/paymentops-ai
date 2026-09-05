import sys
import os

from flask import Flask, render_template, request
import json

sys.path.append(os.path.abspath("src"))

from agent.orchestrator import process_incident


app = Flask(__name__)


SCENARIOS = {

    "network_timeout": {
        "transaction_id": "TXN-TIMEOUT-001",
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
    },

    "risk_decline": {
        "transaction_id": "TXN-RISK-002",
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

    "insufficient_funds": {
        "transaction_id": "TXN-FUNDS-003",
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

    "retry_limit": {
        "transaction_id": "TXN-LIMIT-004",
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

EVALUATION_METRICS = {
    "held_out_incidents": 160,
    "diagnosis_accuracy": 95.00,
    "automatic_actions": 21,
    "payment_retries": 7,
    "successful_recoveries": 6,
    "retry_success_rate": 85.71,
    "simulated_amount_recovered": 100492,
    "unsafe_retries": 0
}

EVALUATION_SUMMARY = [
    {
        "scenario": "Network Timeout",
        "diagnosis": "NETWORK_TIMEOUT",
        "action": "RETRY_PAYMENT",
        "outcome": "Recovered",
        "amount": 12000
    },
    {
        "scenario": "Risk Decline",
        "diagnosis": "RISK_DECLINE",
        "action": "HUMAN_REVIEW",
        "outcome": "Protected",
        "amount": 0
    },
    {
        "scenario": "Insufficient Funds",
        "diagnosis": "INSUFFICIENT_FUNDS",
        "action": "NO_RETRY",
        "outcome": "Retry Avoided",
        "amount": 0
    },
    {
        "scenario": "Retry Limit Reached",
        "diagnosis": "NETWORK_TIMEOUT",
        "action": "HUMAN_REVIEW",
        "outcome": "Safety Stop",
        "amount": 0
    }
]

def get_audit_records():
    audit_file = "data/audit_log.jsonl"

    try:
        with open(audit_file, "r", encoding="utf-8") as file:
            records = [
                json.loads(line)
                for line in file
                if line.strip()
            ]

        return records[-8:][::-1]

    except FileNotFoundError:
        return []


@app.route("/", methods=["GET", "POST"])
def home():

    selected_scenario = request.form.get(
        "scenario",
        "network_timeout"
    )

    incident = SCENARIOS[selected_scenario]

    result = process_incident(incident)

    audit_records = get_audit_records()

    return render_template(
    "dashboard.html",
    incident=incident,
    result=result,
    scenarios=SCENARIOS,
    selected_scenario=selected_scenario,
    audit_records=audit_records,
    metrics=EVALUATION_METRICS,
    evaluation_summary=EVALUATION_SUMMARY
)


if __name__ == "__main__":
    app.run(debug=True)