def send_to_mitra(validated_signal):

    # 🚨 HARD SAFETY CHECK
    if validated_signal["status"] == "REJECT":
        raise Exception("REJECTED signal should NEVER reach Mitra")

    # ✅ ONLY REQUIRED DATA FOR MITRA
    return {
        "signal_id": validated_signal["signal_id"],
        "feature_type": validated_signal["feature_type"],
        "confidence_score": validated_signal["confidence_score"],
        "status": validated_signal["status"]
    }