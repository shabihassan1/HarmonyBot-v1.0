import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = Flask(__name__, static_folder='static', template_folder='templates')

# Hugging Face token
hf_token = "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"

# Load DistilBERT model and tokenizer for classification
distilbert_model_path = r"C:\Users\shabi\my_env\medical_conversational_distilbert"
distilbert_tokenizer = AutoTokenizer.from_pretrained(distilbert_model_path, use_auth_token=hf_token)
distilbert_model = AutoModelForSequenceClassification.from_pretrained(distilbert_model_path, use_auth_token=hf_token)

# Load T5 model and tokenizer for passage retrieval
t5_model_path = r"C:\Users\shabi\my_env\t5_mental_health_finetuned"
t5_tokenizer = AutoTokenizer.from_pretrained(t5_model_path, use_auth_token=hf_token)
t5_model = AutoModelForSeq2SeqLM.from_pretrained(t5_model_path, use_auth_token=hf_token)

# Load SBERT model for passage retrieval
sbert_model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2', use_auth_token=hf_token)

# Check for GPU availability and move models to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
distilbert_model.to(device)
t5_model.to(device)
sbert_model.to(device)

# Load passages for retrieval
passages_path = r"C:\Users\shabi\my_env\ai_medical_chatbot_passages.tsv"
passages = []
with open(passages_path, "r", encoding="utf-8") as file:
    for line in file:
        passages.append(line.strip())

# Encode passages with SBERT
passage_embeddings = sbert_model.encode(passages, convert_to_tensor=True, show_progress_bar=True)
passage_embeddings = passage_embeddings.cpu().detach().numpy()  # Convert to NumPy array for FAISS

# Initialize FAISS index
dimension = passage_embeddings.shape[1]
faiss_index = faiss.IndexFlatIP(dimension)
faiss.normalize_L2(passage_embeddings)
faiss_index.add(passage_embeddings)

# Function to retrieve the most relevant passage using SBERT and FAISS
def retrieve_passage(query):
    query_embedding = sbert_model.encode([query], convert_to_tensor=True).cpu().detach().numpy()
    faiss.normalize_L2(query_embedding)
    distances, indices = faiss_index.search(query_embedding, k=1)
    return passages[indices[0][0]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    # Process user input using the classification model
    inputs = distilbert_tokenizer(user_input, return_tensors="pt").to(device)
    outputs = distilbert_model(**inputs)
    logits = outputs.logits
    predicted_class = logits.argmax().item()
    
    # Depending on the predicted class, choose the appropriate response mechanism
    if predicted_class == 0:  # Assume class 0 is for general conversation
        response_text = "I'm here to help with your general queries."
    else:  # Assume class 1 is for question answering
        passage = retrieve_passage(user_input)
        t5_inputs = t5_tokenizer.encode("question: " + user_input + " context: " + passage, return_tensors="pt").to(device)
        
        # Improved decoding strategy
        t5_outputs = t5_model.generate(
            t5_inputs,
            max_length=150,  # Maximum length of the generated response
            min_length=20,   # Minimum length of the generated response
            num_beams=5,     # Beam search with 5 beams
            repetition_penalty=2.5,  # Penalty for repeating the same tokens
            length_penalty=1.0,  # Controls the length of the output
            early_stopping=True,  # Stop when at least `num_beams` complete sequences are found
            no_repeat_ngram_size=2,  # Prevent repeating n-grams of size 2
            top_p=0.95  # Top-p sampling
        )
        
        response_text = t5_tokenizer.decode(t5_outputs[0], skip_special_tokens=True)
    
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
