from datetime import datetime
import os
from src.validation.dataset_registry import DATASET_REGISTRY

# ---------------- CONSTANTS ----------------
ALLOWED_FEATURE_TYPES = [
    "movement",
    "communication",
    "environmental"
]


# ---------------- LOGGING ----------------
def log_rejected_signal(signal, reason):
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    logs_dir = os.path.join(base_dir, "logs")

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, "rejected_signals.log")

    with open(log_file, "a") as file:
        file.write(
            f"[REJECT] {datetime.now()} | "
            f"SignalID={signal.get('signal_id')} | "
            f"Dataset={signal.get('dataset_id')} | "
            f"Reason={reason}\n"
        )


# ---------------- REJECT ----------------
def reject(signal, reason):
    log_rejected_signal(signal, reason)

    return {
        "signal_id": signal.get("signal_id"),
        "feature_type": signal.get("feature_type"),
        "status": "REJECT",
        "reason": reason,
        "confidence_score": 0.0
    }


# ---------------- CONFIDENCE ----------------
def calculate_confidence(signal):
    score = 1.0

    # Penalize missing value
    if signal.get("value") is None:
        score -= 0.3

    # Dataset trust impact
    dataset_id = str(signal.get("dataset_id"))
    dataset_info = DATASET_REGISTRY.get(dataset_id)

    if dataset_info:
        score *= dataset_info.get("trust_score", 1.0)

    return max(0.0, min(score, 1.0))


# ---------------- VALIDATION ----------------
def validate_signal(signal):

    # 🔴 REQUIRED FIELDS (STRICT CHECK)
    required_fields = ["signal_id", "dataset_id", "timestamp", "feature_type"]

    for field in required_fields:
        if signal.get(field) is None:
            return reject(signal, f"Missing field: {field}")

    # Extract fields
    signal_id = signal.get("signal_id")
    dataset_id = str(signal.get("dataset_id"))
    timestamp = signal.get("timestamp")
    feature_type = signal.get("feature_type")
    value = signal.get("value")
    latitude = signal.get("latitude")
    longitude = signal.get("longitude")

    # 🔴 DATASET VALIDATION
    if dataset_id not in DATASET_REGISTRY:
        return reject(signal, "Invalid value: dataset_id")

    # 🔴 TIMESTAMP VALIDATION
    try:
        ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        if ts > datetime.now():
            return reject(signal, "Invalid value: future timestamp")

    except ValueError:
        return reject(signal, "Invalid format: timestamp")

    # 🔴 LOCATION VALIDATION
    if latitude is None:
        return reject(signal, "Missing field: latitude")

    if not (-90 <= latitude <= 90):
        return reject(signal, "Invalid value: latitude")

    if longitude is None:
        return reject(signal, "Missing field: longitude")

    if not (-180 <= longitude <= 180):
        return reject(signal, "Invalid value: longitude")

    # 🔴 FEATURE TYPE VALIDATION
    if feature_type not in ALLOWED_FEATURE_TYPES:
        return reject(signal, "Invalid value: feature_type")

    # 🔴 VALUE TYPE CHECK
    if value is not None and not isinstance(value, (int, float)):
        return reject(signal, "Invalid value: value must be number or null")

    # 🔴 CONFIDENCE CALCULATION
    confidence = calculate_confidence(signal)

    # 🟡 FLAG CONDITIONS
    if value is None:
        return {
            "signal_id": signal_id,
            "feature_type": feature_type,
            "status": "FLAG",
            "reason": "Suspicious: value is null",
            "confidence_score": confidence
        }

    if confidence < 0.7:
        return {
            "signal_id": signal_id,
            "feature_type": feature_type,
            "status": "FLAG",
            "reason": "Suspicious: low confidence",
            "confidence_score": confidence
        }

    # 🟢 ALLOW
    return {
        "signal_id": signal_id,
        "feature_type": feature_type,
        "status": "ALLOW",
        "reason": "Valid signal",
        "confidence_score": confidence
    }