# REVIEW_PACKET.md

## 🔷 Project: Signal Validation & Trust Enforcement Layer

---

## ✅ 1. Entry Point

The system starts from:

* `run_demo_validation.py` (for testing/demo)
* `/validate` API endpoint (FastAPI)

The flow begins with **raw Samachar event input**, ensuring no pre-processed data bypasses validation.

---

## 🔷 2. Validation Flow

```
Samachar Event (raw input)
        ↓
samachar_to_signal (Adapter Layer)
        ↓
validate_signal (Validation Layer)
        ↓
Pipeline Enforcement (Decision Control)
        ↓
Mitra (Consumer System)
        ↓
UI Output (Structured Response)
```

---

## 🔷 3. Core Components

### 📁 dataset_registry.py

* Stores dataset metadata
* Validates dataset_id
* Controls trust_score
* Blocks inactive datasets

---

### 📁 signal_validator.py

* Validates:

  * dataset_id
  * timestamp
  * latitude / longitude
  * feature_type
  * value type
* Assigns:

  * ALLOW / FLAG / REJECT
  * confidence_score
* Logs rejected signals

---

### 📁 samachar_adapter.py

* Converts raw event → signal format
* Enforces required fields
* Prevents malformed or incomplete data

---

### 📁 pipeline.py

* Enforces strict validation (non-bypassable)
* Ensures validation before any processing
* Stops execution on REJECT
* Forwards only ALLOW/FLAG signals

---

### 📁 mitra_interface.py

* Receives only validated signals
* Accepts:

  * signal_id
  * feature_type
  * confidence_score
  * status

---

### 📁 api/main.py

* FastAPI endpoint: `POST /validate`
* Accepts raw input
* Returns structured, UI-ready response
* Handles validation errors via HTTP responses

---

## 🔷 4. Decision Logic

| Status | Meaning               |
| ------ | --------------------- |
| ALLOW  | Valid signal          |
| FLAG   | Suspicious but usable |
| REJECT | Invalid (blocked)     |

---

### Risk Mapping

| Confidence | Risk   |
| ---------- | ------ |
| ≥ 0.8      | LOW    |
| 0.7–0.79   | MEDIUM |
| < 0.7      | HIGH   |

---

### Action Mapping

| Status | Action  |
| ------ | ------- |
| ALLOW  | PROCEED |
| FLAG   | REVIEW  |
| REJECT | BLOCK   |

---

## 🔷 5. Failure Handling

* Missing fields → Exception
* Invalid dataset → REJECT
* Future timestamp → REJECT
* Invalid coordinates → REJECT
* Invalid data types → REJECT

👉 System behavior:

* No silent failures
* No assumptions on missing data
* Immediate rejection of invalid inputs

⚠️ **Critical Enforcement:**
If a signal is REJECTED, the pipeline immediately stops execution and the API returns an error response.
This ensures that no invalid data propagates to downstream systems.

---

## 🔷 6. Logging

File:

```
logs/rejected_signals.log
```

Each rejected signal logs:

* timestamp
* signal_id
* dataset_id
* reason

---

## 🔷 7. Sample Input

```json
{
  "id": 1,
  "time": "2025-03-25 10:30:00",
  "lat": 28.6,
  "lon": 77.2,
  "type": "movement",
  "value": 10,
  "dataset_id": "1"
}
```

---

## 🔷 8. Sample Output

```json
{
  "input_summary": "Signal 1 processed",
  "validation": {
    "status": "ALLOW",
    "confidence": 0.9,
    "reason": "Valid signal"
  },
  "decision": {
    "risk": "LOW",
    "action": "PROCEED"
  }
}
```

---

## 🔷 9. Test Cases

| Case               | Expected Output |
| ------------------ | --------------- |
| Missing dataset_id | REJECT          |
| Future timestamp   | REJECT          |
| Null value         | FLAG            |
| Valid signal       | ALLOW           |

---

## 🔷 10. System Guarantees

✔ No invalid data enters the system
✔ All signals are validated before use
✔ REJECT immediately stops execution
✔ FLAG signals are handled safely
✔ Full traceability via logs
✔ Clean structured output for UI

---

## 🔷 11. Integration Points

| Component | Role              |
| --------- | ----------------- |
| Samachar  | Input provider    |
| Validator | Trust enforcement |
| Mitra     | Decision consumer |
| UI        | Output display    |

---

## 🔷 12. API Exposure

The system is exposed via a FastAPI endpoint:

```
POST /validate
```

It accepts raw input and returns a validated, structured response suitable for frontend/UI integration.

---

## 🔷 13. Final Outcome

This system implements a **strict trust boundary layer** that:

* Prevents invalid data entry
* Ensures deterministic processing
* Maintains system reliability
* Enforces validation across all components

---

## 🚀 Conclusion

The project successfully transforms a basic validation module into a **fully enforced trust layer**, ensuring correctness, traceability, and reliability across the entire pipeline.
