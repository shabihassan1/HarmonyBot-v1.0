from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

model_name = "distilbert-base-uncased-distilled-squad"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForQuestionAnswering.from_pretrained(model_name)

# Create dummy input for the model
dummy_input = tokenizer("What is your name?", "My name is ChatGPT", return_tensors="pt")

# Export the model to ONNX format
torch.onnx.export(model, 
                  (dummy_input['input_ids'], dummy_input['attention_mask']), 
                  "distilbert_qa.onnx", 
                  input_names=['input_ids', 'attention_mask'], 
                  output_names=['start_logits', 'end_logits'], 
                  dynamic_axes={'input_ids': {0: 'batch_size', 1: 'sequence'}, 
                                'attention_mask': {0: 'batch_size', 1: 'sequence'}, 
                                'start_logits': {0: 'batch_size', 1: 'sequence'}, 
                                'end_logits': {0: 'batch_size', 1: 'sequence'}})
