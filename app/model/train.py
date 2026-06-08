import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

def train():
    fake = pd.read_csv("data/Fake.csv")
    true = pd.read_csv("data/True.csv")

    fake["label"] = 0  # 0 = фейк
    true["label"] = 1  # 1 = правда

    df = pd.concat([fake[:2500], true[:2500]])
    df = df[["title", "label"]].dropna()
    X_train, X_test, y_train, y_test = train_test_split(
        df["title"], df["label"], test_size=0.2, random_state=42
    )

    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test_vec))
    print(f"Accuracy: {accuracy:.2f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    print("model saved!")

if __name__ == "__main__":
    train()
