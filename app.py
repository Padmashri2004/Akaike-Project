from flask import Flask, request, jsonify
import joblib
import re

# Load model and vectorizer
vectorizer = joblib.load("vectorizer.pkl")
model = joblib.load("rf_model.pkl")

REGEX_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone_number": r"\b(?:\+?91[-\s]?)?[6-9]\d{9}\b",
    "dob": r"\b(?:0?[1-9]|[12][0-9]|3[01])[/\-](?:0?[1-9]|1[012])[/\-](?:\d{2,4})\b",
    "aadhar_num": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3,4}\b",
    "expiry_no": r"\b(?:0?[1-9]|1[012])/?\d{2,4}\b",
    "full_name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"
}

def pii_mask(text: str):
    spans = []
    for label, pattern in REGEX_PATTERNS.items():
        for m in re.finditer(pattern, text):
            spans.append((m.start(), m.end(), label))

    spans = sorted(set(spans), key=lambda x: x[0])
    masked, cursor = [], 0
    entity_map = []

    for start, end, label in spans:
        masked.append(text[cursor:start])
        masked.append(f"[{label}]")
        entity_map.append({
            "position": [start, end],
            "classification": label,
            "entity": text[start:end]
        })
        cursor = end
    masked.append(text[cursor:])
    return "".join(masked), entity_map

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify_email():
    data = request.get_json(force=True)
    input_email = data.get('input_email_body', '')

    masked_email, entity_map = pii_mask(input_email)
    vec_input = vectorizer.transform([masked_email])
    pred = model.predict(vec_input)[0]

    return jsonify({
        "input_email_body": input_email,
        "list_of_masked_entities": entity_map,
        "masked_email": masked_email,
        "category_of_the_email": pred
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
