import os
from flask import Flask, request, jsonify
from utils import pii_mask
from models import classify_email

app = Flask(__name__)

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json(force=True)
    if not data or "input_email_body" not in data:
        return jsonify({"error": "Field 'input_email_body' missing"}), 400

    input_email = data["input_email_body"]
    masked_email, entities = pii_mask(input_email)
    category = classify_email(masked_email)

    return jsonify(
        {
            "input_email_body": input_email,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": category,
        }
    )

# Hugging Face looks for 'app' object, but running locally needs __main__
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
