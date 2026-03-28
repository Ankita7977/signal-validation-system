import sys
import os

# 🔧 Fix import path
sys.path.append(
    os.path.abspath(os.path.dirname(__file__))
)

from src.pipeline import run_pipeline


# 🔥 SAMACHAR RAW INPUT (CORRECT FORMAT)
signals = [

    # ✅ VALID SIGNAL (ALLOW)
    {
        "id": 1,
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 10,
        "dataset_id": "1"
    },

    # ⚠️ FLAG CASE (value = None)
    {
        "id": 2,
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": None,
        "dataset_id": "2"
    },

    # ❌ REJECT CASE (future timestamp)
    {
        "id": 3,
        "time": "2035-01-01 10:00:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 20,
        "dataset_id": "1"
    },

    # ❌ REJECT CASE (invalid dataset)
    {
        "id": 4,
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 15,
        "dataset_id": "999"
    }
]


# 🚀 RUN PIPELINE
try:
    results = run_pipeline(signals)
    print("\n✅ FINAL OUTPUT:\n")
    for res in results:
        print(res)

except Exception as e:
    print("\n❌ PIPELINE ERROR:\n", str(e))