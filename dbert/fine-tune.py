import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset

# Load the original dataset directly
dataset = load_dataset("avaliev/chat_doctor", split="train")

# Initialize the tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Convert the 'output' to a binary label based on specific conditions
def preprocess_function(examples):
    inputs = tokenizer(
        examples['input'], truncation=True, padding="max_length", max_length=256
    )
    # Convert the output into binary labels (this is just a placeholder logic)
    # Adjust this logic based on your actual task requirements.
    # For example: 
    # inputs['labels'] = [1 if "urgent" in output else 0 for output in examples['output']]
    # You may need to adjust this according to your dataset's needs.
    inputs['labels'] = [0 if len(output) < 50 else 1 for output in examples['output']]  # Example condition
    return inputs

# Tokenize the dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Data collator for dynamic padding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Set training arguments
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=3,  # Adjust based on dataset size and requirements
    per_device_train_batch_size=16,  # Use appropriate batch size for your hardware
    per_device_eval_batch_size=16,
    save_steps=10_000,
    save_total_limit=2,
    eval_strategy="steps",  # Updated from deprecated `evaluation_strategy`
    eval_steps=1000,  # Evaluate every 1000 steps
    fp16=True,  # Enable mixed precision training for faster training
    logging_dir='./logs',
    logging_steps=100,  # Log every 100 steps
    learning_rate=2e-5,  # Fine-tune learning rate if needed
    warmup_steps=500,  # Warmup steps for learning rate scheduler
    weight_decay=0.01,  # Weight decay to prevent overfitting
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,  # Use the entire tokenized dataset
    eval_dataset=tokenized_dataset,  # Assuming validation split is done manually or not needed
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Start training
trainer.train()

# Save the trained model
trainer.save_model("./medical_conversational_bert")
