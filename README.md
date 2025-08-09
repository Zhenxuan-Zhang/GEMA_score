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

### 2️⃣ Run Locally with HuggingFace Transformers
We provide distilled models for CT and X-ray evaluation.
HuggingFace model hub: https://huggingface.co/Gemascore/GEMA-Score-distilled
```bash
pip install transformers accelerate torch
```
```python
import torch
from transformers import AutoModelForCausalLM, AutoProcessor

# Model repo & subfolder (choose CT or Xray version)
REPO_ID = "Gemascore/GEMA-Score-distilled"
SUBFOLDER = "GEMA-Score-distilled-CT-llama"  # Options: 
# "GEMA-Score-distilled-CT-llama"
# "GEMA-Score-distilled-CT-Qwen"
# "GEMA-Score-distilled-Xray-llama"
# "GEMA-Score-distilled-Xray-Qwen"

# Load model & processor
model = AutoModelForCausalLM.from_pretrained(
    REPO_ID,
    subfolder=SUBFOLDER,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    trust_remote_code=True
)

processor = AutoProcessor.from_pretrained(
    REPO_ID,
    subfolder=SUBFOLDER,
    trust_remote_code=True
)

# Example inference
prompt = """
Evaluate the following reports in JSON format.
Candidate: 'No focal areas of consolidation.'
Reference: 'The heart is normal in size. The lungs are clear.'
"""

inputs = processor(text=prompt, return_tensors="pt").to(model.device)
output_ids = model.generate(**inputs, max_new_tokens=1024)
output_text = processor.batch_decode(output_ids, skip_special_tokens=True)[0]
print(output_text)
```
---

## 🔥 Contribution Guide
We welcome issues and pull requests to improve **GEMA-Score
