import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "models" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "vectorizer.pkl"

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    model = None
    vectorizer = None
    print(f"Warning: model not found at {MODEL_PATH}")

def predict(text: str) -> dict:
    if model is None or vectorizer is None:
        return {
            "label": "UNKNOWN",
            "confidence": 0.0,
            "passed_quality_gate": False
        }
    vec = vectorizer.transform([text])
    label = model.predict(vec)[0]
    confidence = model.predict_proba(vec)[0].max()
    
    return {
        "label": "REAL" if label == 1 else "FAKE",
        "confidence": round(float(confidence), 2),
        "passed_quality_gate": bool(confidence > 0.7)
    }
    