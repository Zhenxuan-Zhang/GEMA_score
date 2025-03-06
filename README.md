# GEMA-Score: Granular Explainable Multi-Agent Score for Radiology Report Evaluation

![GEMA-Score](https://img.shields.io/badge/GEMA-Score-blue.svg)
![License](https://img.shields.io/github/license/your-repo/GEMA-Score)

## 🚀 Project Overview

**GEMA-Score** is a medical report evaluation tool designed to provide a **granular, explainable, multi-agent scoring** mechanism for automated medical report assessment. It integrates **LLM (Large Language Model)** and **Multi-Agent Evaluation Strategy**, ensuring the assessment not only covers **key medical information** but also evaluates **lesion location, severity, medical terminology, and readability**.

> 🎯 Online Demo: [GEMA-Score Demo](https://udify.app/chat/jPOWanLUMb0NAeKI)

## ✨ Features
- ✅ **Multi-Agent Scoring Architecture**: Includes entity extraction, objective clinical accuracy, subjective expressiveness, and overall evaluation agents.
- 🔍 **Explainable Scoring**: Combines NER-F1, medical terminology consistency, LLM-based scoring, and more.
- 🤖 **Easy Deployment with Dify**: Leverages LLM for a more reliable automated evaluation.
- 📊 **Validated High Correlation**: Achieves Kendall correlation of 0.70 on Rexval dataset and 0.54 on RadEvalX dataset.

---

## 📦 Installation & Deployment

### 1️⃣ Use Listed Endpoint (Recommended)
```bash
# Use Python to request GEMA-Score API
pip install requests

import requests

url = "https://udify.app/chat/jPOWanLUMb0NAeKI"
data = {"input": "your medical report text"}
headers = {"Authorization": "Bearer YOUR_API_KEY"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 2️⃣ Local Deployment (Docker)
```bash
git clone https://github.com/your-repo/GEMA-Score.git
cd GEMA-Score
docker-compose up -d
```

---

## 📖 Usage Example

```python
import requests

url = "http://localhost:8000/score"
data = {"report": "Chest X-ray shows mild pleural effusion ..."}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

---

## 🔥 Contribution Guide
We welcome issues and pull requests to improve **GEMA-Score
