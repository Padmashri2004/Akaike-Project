import joblib

# Load on module import (only once)
model = joblib.load("rf_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def classify_email(masked_email: str) -> str:
    """Return category string."""
    vec = vectorizer.transform([masked_email])
    return model.predict(vec)[0]
