def samachar_to_signal(event):

    # 🚨 HARD VALIDATION (NO SILENT FAILURES)
    required_fields = ["id", "time", "lat", "lon", "type", "dataset_id"]

    for field in required_fields:
        if field not in event or event.get(field) is None:
            raise Exception(f"Samachar input error: Missing field: {field}")

    # 🔴 TYPE VALIDATION
    if not isinstance(event["time"], str):
        raise Exception("Samachar input error: Invalid type for time")

    try:
        latitude = float(event["lat"])
        longitude = float(event["lon"])
    except (ValueError, TypeError):
        raise Exception("Samachar input error: lat/lon must be numeric")

    # Optional: dataset_id normalization
    dataset_id = str(event["dataset_id"])

    # Optional: value type check
    value = event.get("value")
    if value is not None and not isinstance(value, (int, float)):
        raise Exception("Samachar input error: value must be number or null")

    # ✅ SAFE MAPPING
    signal = {
        "signal_id": event["id"],
        "timestamp": event["time"],
        "latitude": latitude,
        "longitude": longitude,
        "feature_type": event["type"],
        "value": value,
        "dataset_id": dataset_id
    }

    return signal