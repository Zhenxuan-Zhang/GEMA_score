import pandas as pd
from transformers import AutoModelForCausalLM, AutoProcessor
import torch
import json
from tqdm import tqdm
import re

def extract_json_between_keys(text, start_key="\"entity_name false_prediction\"", end_key="\"true_positive_matches\""):
    """
    Extract a JSON object from a text, starting at start_key and ending when the
    corresponding closing brace for the end_key is found.
    Returns a Python dictionary.
    """
    start_key_idx = text.find(start_key)
    if start_key_idx == -1:
        raise ValueError(f"Start key '{start_key}' not found.")
    start_brace_idx = text.rfind('{', 0, start_key_idx)
    if start_brace_idx == -1:
        raise ValueError("No '{' found before start key.")
    end_key_idx = text.find(end_key, start_key_idx)
    if end_key_idx == -1:
        raise ValueError(f"End key '{end_key}' not found.")

    # Use a stack to match braces and find the complete JSON object
    stack = []
    for i in range(start_brace_idx, len(text)):
        if text[i] == '{':
            stack.append('{')
        elif text[i] == '}':
            if stack:
                stack.pop()
            if not stack:
                json_str = text[start_brace_idx:i+1]
                return json.loads(json_str)
    raise ValueError("No complete JSON object found.")

# ==== Model path (Hugging Face Hub) ====
# Change to the desired model, e.g.:
REPO_ID = "Gemascore/GEMA-Score-distilled"
SUBFOLDER = "GEMA-Score-distilled-CT-llama"   # ← CT 
# SUBFOLDER = "GEMA-Score-distilled-Xray-llama" # ← X-ray 
# SUBFOLDER = "GEMA-Score-distilled-CT-Qwen" # ← CT Qwen 
# SUBFOLDER = "GEMA-Score-distilled-Xray-Qwen" # ← X-ray Qwen

model = AutoModelForCausalLM.from_pretrained(
    REPO_ID,
    subfolder=SUBFOLDER,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    trust_remote_code=True, 
)

# Load processor (tokenizer + preprocessor)
processor = AutoProcessor.from_pretrained(model_dir)

# ==== Load input CSV ====
input_file = "combined_method(2).csv"
df = pd.read_csv(input_file)

# ==== Create new columns if not exist ====
if "eval_result" not in df.columns:
    df["eval_result"] = ""
if "weighted_final_score" not in df.columns:
    df["weighted_final_score"] = None

# ==== Iterate through each row ====
for i in tqdm(range(len(df))):
    # Skip if already processed (allows resume after interruption)
    if pd.notnull(df.loc[i, "weighted_final_score"]):
        continue

    pred = str(df.loc[i, "output_validation_ctchat_8b_retrain"]).strip()
    gt = str(df.loc[i, "gt"]).strip()

    # JSON schema template (escaped double quotes for LLM output)
    json_schema = r"""
    \n\n{\"entity_name false_prediction\": <int>, \"entity_name false_prediction_explanation\": <string>, \"entity_name omission\": <int>, \"entity_name omission_explanation\": <string>, \"location false_prediction\": <int>, \"location false_prediction_explanation\": <string>, \"location omission\": <int>, \"location omission_explanation\": <string>, \"severity false_prediction\": <int>, \"severity false_prediction_explanation\": <string>, \"severity omission\": <int>, \"severity omission_explanation\": <string>, \"uncertainty false_prediction\": <int>, \"uncertainty false_prediction_explanation\": <string>, \"uncertainty omission\": <int>, \"uncertainty omission_explanation\": <string>, \"completeness_score\": <float>, \"completeness_reason\": <string>, \"readability_score\": <float>, \"readability_reason\": <string>, \"clinical_utility_score\": <float>, \"clinical_utility_reason\": <string>, \"weighted_final_score\": <float>}
    """
    
    # Construct the final prompt
    prompt = f"""
    user Evaluate the accuracy of a candidate radiology report in comparison to a reference radiology report composed by expert radiologists. You should determine the following aspects and return the result as a **stringified JSON object** in exactly this format (with escaped double quotes):
    {json_schema}
    
    Only output the stringified JSON object. Do not add explanations, markdown, or formatting.
    
    Candidate radiology report:
    {pred}
    
    Reference radiology report:
    {gt}
    """
    
    try:
        # Tokenize and prepare input
        inputs = processor(text=prompt, return_tensors="pt").to(model.device)
        
        # Generate output from the model
        output_ids = model.generate(
            **inputs,
            max_new_tokens=2048,
            repetition_penalty=1.2,
        )
    
        # Decode model output
        output_text = processor.batch_decode(output_ids, skip_special_tokens=True)[0]
        
        # Extract JSON result from model output
        result = extract_json_between_keys(
            output_text,
            start_key="\"entity_name false_prediction\"",
            end_key="\"true_positive_matches\""
        )
    
        # Get weighted final score from the extracted JSON
        score = result.get("weighted_final_score", None)
    
    except Exception as e:
        # Save error details
        result = {
            "error": str(e),
            "raw_output": output_text if "output_text" in locals() else "N/A"
        }
        score = None
    
    # Store results in DataFrame
    df.loc[i, "eval_result"] = json.dumps(result, ensure_ascii=False)
    df.loc[i, "weighted_final_score"] = score
    
    # Save after each row to allow resume in case of interruption
    df.to_csv(input_file, index=False)
