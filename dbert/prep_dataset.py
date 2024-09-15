import warnings
import os
import pandas as pd
import numpy as np
from datasets import Dataset, load_dataset
from sentence_transformers import SentenceTransformer
import faiss
from huggingface_hub import login
from joblib import Parallel, delayed

warnings.filterwarnings('ignore', category=FutureWarning)

# Set environment variables and authenticate with Hugging Face
login(token="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")

# Load the dataset
dataset = load_dataset("avaliev/chat_doctor")
df = pd.DataFrame(dataset['train'])

# Initialize embedding model using SentenceTransformer
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

# Compute embeddings for all documents
embeddings = embedding_model.encode(df['input'].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings, dtype=np.float32)
faiss.normalize_L2(embeddings)

# Save embeddings to disk
np.save("embeddings.npy", embeddings)
df.to_csv("dataset.csv", index=False)

# Initialize FAISS index and add embeddings
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Batch retrieval of similar examples
def batch_retrieve_similar_examples(batch_indices, k=5):
    batch_inputs = df.loc[batch_indices, 'input'].tolist()
    batch_embeddings = embedding_model.encode(batch_inputs)
    faiss.normalize_L2(batch_embeddings)
    distances, indices = index.search(np.array(batch_embeddings, dtype=np.float32), k)
    
    augmented_examples = []
    for i, idx in enumerate(batch_indices):
        example = df.iloc[idx]
        similar_examples = [df.iloc[sim_idx] for sim_idx in indices[i]]
        for sim_example in similar_examples:
            augmented_example = {
                'input': example['input'] + " [SEP] " + sim_example['input'],
                'output': sim_example['output']
            }
            augmented_examples.append(augmented_example)
    return augmented_examples

# Parallel processing of dataset to speed up augmentation
def augment_dataset_parallel(df, k=5, batch_size=100):
    n_jobs = os.cpu_count()  # Use all available cores
    indices = range(len(df))
    results = Parallel(n_jobs=n_jobs)(
        delayed(batch_retrieve_similar_examples)(indices[i:i + batch_size], k)
        for i in range(0, len(indices), batch_size)
    )
    
    # Flatten the list of lists
    augmented_examples = [item for sublist in results for item in sublist]
    return Dataset.from_pandas(pd.DataFrame(augmented_examples))

# Augment the dataset
augmented_dataset = augment_dataset_parallel(df)

# Save the augmented dataset
augmented_dataset.save_to_disk("augmented_dataset")

print("Dataset preprocessing completed. Embeddings, FAISS index, and augmented dataset saved.")
