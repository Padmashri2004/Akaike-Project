# Email Classification API (Flask)

Support-team emails are:
- **PII-masked** with regex rules
- Classified into **Incident / Request / Change / Problem** using a TF-IDF + Random Forest model

## 🔧 Setup (local)

```bash
git clone https://github.com/<your-username>/email-classifier.git
cd email-classifier
pip install -r requirements.txt
python main.py          # runs on http://localhost:7860/classify
