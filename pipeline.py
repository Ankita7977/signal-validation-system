from src.validation.signal_validator import validate_signal
from src.mitra.mitra_interface import send_to_mitra
from src.samachar_adapter import samachar_to_signal


def get_risk_level(confidence):
    if confidence >= 0.8:
        return "LOW"
    elif confidence >= 0.7:
        return "MEDIUM"
    else:
        return "HIGH"


def get_action(status):
    if status == "ALLOW":
        return "PROCEED"
    elif status == "FLAG":
        return "REVIEW"
    else:
        return "BLOCK"


def run_pipeline(events):

    results = []

    for event in events:

        # 🔁 STEP 1: Samachar → Signal
        signal = samachar_to_signal(event)

        # 🚨 STEP 2: VALIDATION (MANDATORY)
        validation = validate_signal(signal)

        # 🚨 STEP 3: HARD STOP IF REJECT
        if validation["status"] == "REJECT":
            print("❌ REJECTED:", validation)
            raise Exception("Validation failed. Pipeline stopped.")

        # ✅ STEP 4: Send ONLY validated data to Mitra
        mitra_data = send_to_mitra(validation)

        # 🎯 STEP 5: Decision Layer
        risk = get_risk_level(validation["confidence_score"])
        action = get_action(validation["status"])

        # ✅ STEP 6: UI OUTPUT FORMAT
        results.append({
            "input_summary": f"Signal {validation['signal_id']} processed",
            "validation": {
                "status": validation["status"],
                "confidence": validation["confidence_score"],
                "reason": validation["reason"]
            },
            "decision": {
                "risk": risk,
                "action": action
            }
        })

    return results