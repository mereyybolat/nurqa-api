import joblib

model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def predict(text: str) -> dict:
    vec = vectorizer.transform([text])
    label = model.predict(vec)[0]
    confidence = model.predict_proba(vec)[0].max()

    return {
        "label": "REAL" if label == 1 else "FAKE",
        "confidence": round(float(confidence), 2),
        "passed_quality_gate": bool(confidence > 0.7)
    }
