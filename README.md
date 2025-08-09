# GEMA-Score: Granular Explainable Multi-Agent Score for Radiology Report Evaluation

![GEMA-Score](https://img.shields.io/badge/GEMA-Score-blue.svg)
![License](https://img.shields.io/github/license/your-repo/GEMA-Score)

## 🚀 Overview  
**GEMA-Score** is a medical report evaluation framework that delivers **granular, explainable, multi-agent scoring** for automated medical report assessment.  
By combining **Large Language Models (LLMs)** with a **Multi-Agent Evaluation Strategy**, it evaluates both the **clinical accuracy** and the **linguistic quality** of medical reports.

Key evaluation aspects include:  
- **Key Medical Findings** — Coverage and correctness of critical diagnostic information.  
- **Lesion Location** — Accuracy of anatomical positioning.  
- **Severity Assessment** — Correct grading of disease severity.  
- **Medical Terminology** — Proper and precise use of medical terms.  
- **Readability & Clarity** — Language quality for clinical communication.  

---

## 🌐 Online Demos

We provide two specialized demo versions:  

| Version | Target Modality | Demo Link |
|---------|-----------------|-----------|
| **X-ray Report Evaluation** | Chest X-ray reports | [🔗 Try Here](https://udify.app/chat/jPOWanLUMb0NAeKI) |
| **CT Report Evaluation** | CT scan reports | [🔗 Try Here](https://udify.app/chat/KPay0RAm34UfMbG4) |

---

## ✨ Features
- ✅ **Multi-Agent Scoring Architecture**: Includes entity extraction, objective clinical accuracy, subjective expressiveness, and overall evaluation agents.
- 🔍 **Explainable Scoring**: Combines NER-F1, medical terminology consistency, LLM-based scoring, and more.
- 🤖 **Easy Deployment with Dify**: Leverages LLM for a more reliable automated evaluation.
- 📊 **Validated High Correlation**: Achieves Kendall correlation of 0.70 on Rexval dataset and 0.54 on RadEvalX dataset.

---

## 📦 Installation & Deployment

### 1️⃣ Use Listed Endpoint (Recommended)
```bash
# Install required Python package
pip install requests
```
```python
import requests

# Dify API Configuration
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = "YOUR_API_KEY"

# Example input medical reports
data = {
    "inputs": {
        "GroundTruth_medical_report": "The heart is normal in size. The lungs are clear.",
        "Candidate_medical_report": "No focal areas of consolidation. No pleural effusions."
    },
    "query": "Evaluate these medical reports.",
    "user": "user-123",
    "response_mode": "blocking"
}

# Set request headers
headers = {
    "Authorization": f"Bearer {DIFY_API_KEY}",
    "Content-Type": "application/json"
}

# Send request to Dify API
response = requests.post(DIFY_API_URL, json=data, headers=headers)
print(response.json())  # Print the response
```

---

### 2️⃣ Local Deployment (Docker)
```bash
git clone https://github.com/your-repo/GEMA-Score.git
cd GEMA-Score
docker-compose up -d
```

---

## 📚 Usage Example (Local API)
```python
import requests

# Local API Configuration
url = "http://localhost:8000/score"
data = {"report": "Chest X-ray shows mild pleural effusion ..."}
headers = {"Content-Type": "application/json"}

# Send request to local API
response = requests.post(url, json=data, headers=headers)
print(response.json())  # Print the response
```

---

## 🔥 Contribution Guide
We welcome issues and pull requests to improve **GEMA-Score
