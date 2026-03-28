# Signal Validation & Trust Enforcement System

## 📌 Project Overview

This project implements a **strict data validation and trust enforcement layer** to ensure that no invalid data enters the system.

It validates incoming signals, assigns confidence scores, and enforces decision logic before allowing data to flow to downstream systems.

---

## 🎯 Objective 

To build a **reliable and strict validation system** that:

* Prevents invalid data entry
* Flags suspicious data
* Ensures trusted data flow

---

## ⚙️ System Flow

```
Samachar (Input)
    ↓
Adapter (samachar_to_signal)
    ↓
Validation Layer (signal_validator)
    ↓
Pipeline Control
    ↓
Mitra (Decision System)
    ↓
UI Output
```

---

## 🚦 Validation Decisions

| Status | Description           |
| ------ | --------------------- |
| ALLOW  | Valid signal          |
| FLAG   | Suspicious but usable |
| REJECT | Invalid (blocked)     |

---

## 📊 Features

* ✅ Dataset Registry Validation
* ✅ Confidence Scoring System
* ✅ Strict Pipeline Enforcement
* ✅ No Validation Bypass
* ✅ Logging of Rejected Signals
* ✅ FastAPI Endpoint for Integration

---

## 🔌 API Endpoint

```
POST /validate
```

* Accepts raw input (Samachar event)
* Returns validated, structured response

---

## 🧪 Test Cases

* Missing dataset_id → REJECT
* Future timestamp → REJECT
* Null value → FLAG
* Valid signal → ALLOW

---

## 📁 Project Structure

```
src/
 ├── validation/
 │    ├── signal_validator.py
 │    ├── dataset_registry.py
 │
 ├── pipeline.py
 ├── samachar_adapter.py
 │
 ├── mitra/
 │    ├── mitra_interface.py
 │
 ├── api/
 │    ├── main.py

logs/
 ├── rejected_signals.log

run_demo_validation.py
REVIEW_PACKET.md
```

---

## ▶️ How to Run

### 1. Install dependencies

```
pip install fastapi uvicorn
```

### 2. Run API

```
python -m uvicorn src.api.main:app --reload
```

### 3. Open in browser

```
http://127.0.0.1:8000/docs
```

---

## 🧠 Key Guarantee

> No invalid data is allowed to enter the system.
> The pipeline strictly enforces validation before processing.

---

## 🚀 Conclusion

This system ensures **data integrity, reliability, and trust**, making it suitable for real-world decision systems.
