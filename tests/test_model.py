import pandas as pd
import pytest
import joblib
from sklearn.metrics import accuracy_score

model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

fake = pd.read_csv("data/Fake.csv")
true = pd.read_csv("data/True.csv")

fake["label"] = 0
true["label"] = 1
df = pd.concat([fake[:2500], true[:2500]])[["title", "label"]].dropna()

def test_features_present():
    assert "title" in df.columns
    assert "label" in df.columns

def test_accuracy_above_threshold():
    X=vectorizer.transform(df["title"])
    preds = model.predict(X)
    acc = accuracy_score(df["label"], preds)
    assert acc>0.7, f"Accuracy {acc} is below threshold {acc}"

def test_model_determenistic():
    text=["Breaking news about election"]
    result1=model.predict(vectorizer.transform(text))
    result2=model.predict(vectorizer.transform(text))
    assert result1[0]==result2[0]

def test_no_data_drift():
    fake_len=len(fake[:2500].dropna())
    true_len=len(true[:2500].dropna())
    ratio = fake_len/true_len
    assert 0.8<ratio<1.2, "disbalance between fake&true"
