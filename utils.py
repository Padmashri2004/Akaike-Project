import re

REGEX_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone_number": r"\b(?:\+?91[-\s]?)?[6-9]\d{9}\b",
    "dob": r"\b(?:0?[1-9]|[12][0-9]|3[01])[/\-](?:0?[1-9]|1[012])[/\-](?:\d{2,4})\b",
    "aadhar_num": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3,4}\b",
    "expiry_no": r"\b(?:0?[1-9]|1[012])/?\d{2,4}\b",
    "full_name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b",
}

def pii_mask(text: str):
    """Mask PII, return (masked_text, list_of_entities)."""
    spans = []
    for label, pat in REGEX_PATTERNS.items():
        for m in re.finditer(pat, text):
            spans.append((m.start(), m.end(), label))

    spans = sorted({(s, e, l) for s, e, l in spans}, key=lambda x: x[0])  # dedupe
    masked_parts, mapping, cursor = [], [], 0

    for start, end, label in spans:
        masked_parts.append(text[cursor:start])
        masked_parts.append(f"[{label}]")
        mapping.append(
            {
                "position": [start, end],
                "classification": label,
                "entity": text[start:end],
            }
        )
        cursor = end

    masked_parts.append(text[cursor:])
    return "".join(masked_parts), mapping
