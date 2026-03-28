# ---------------- DATASET REGISTRY ----------------

DATASET_REGISTRY = {
    "1": {
        "source": "trusted",
        "trust_score": 0.9,
        "status": "active",
        "description": "Government verified dataset"
    },
    "2": {
        "source": "medium",
        "trust_score": 0.6,
        "status": "active",
        "description": "Third-party dataset"
    },
    "3": {
        "source": "low",
        "trust_score": 0.4,
        "status": "inactive",
        "description": "Deprecated dataset"
    }
}


# ---------------- VALIDATION FUNCTION ----------------

def is_valid_dataset(dataset_id):
    dataset = DATASET_REGISTRY.get(str(dataset_id))

    if not dataset:
        return False, "Dataset not found"

    if dataset.get("status") != "active":
        return False, "Dataset is inactive"

    return True, dataset


# ---------------- OPTIONAL HELPER ----------------

def get_dataset_trust_score(dataset_id):
    dataset = DATASET_REGISTRY.get(str(dataset_id))

    if not dataset:
        return 0.0

    return dataset.get("trust_score", 0.0)