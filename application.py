import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from huggingface_hub import InferenceClient
from datasets import load_dataset
import markdown2

# Set up Hugging Face cache
os.environ["HF_HOME"] = "/app/.cache"

# Initialize FastAPI application
app = FastAPI()

# Set up templates and static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Hugging Face API token
hf_token = os.getenv("HF_TOKEN")

# Load datasets
chat_doctor_dataset = load_dataset("avaliev/chat_doctor")
mental_health_dataset = load_dataset("Amod/mental_health_counseling_conversations")

# Set up Hugging Face Inference Client
client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token=hf_token,
)

def select_relevant_context(user_input: str) -> str:
    """Select relevant context from the datasets based on user input keywords."""
    mental_health_keywords = [
        "anxious", "depressed", "stress", "mental health", "counseling", 
        "therapy", "feelings", "worthless", "suicidal", "panic", "anxiety"
    ]
    medical_keywords = [
        "symptoms", "diagnosis", "treatment", "doctor", "prescription", "medication",
        "pain", "illness", "disease", "infection", "surgery"
    ]

    if any(keyword in user_input.lower() for keyword in mental_health_keywords):
        example = mental_health_dataset['train'][0]
        context = f"Counselor: {example['Response']}\nUser: {example['Context']}"
    elif any(keyword in user_input.lower() for keyword in medical_keywords):
        example = chat_doctor_dataset['train'][0]
        context = f"Doctor: {example['input']}\nPatient: {example['output']}"
    else:
        context = "You are a general assistant. Respond to the user's query in a helpful manner."
    
    return context

def create_prompt(context: str, user_input: str) -> str:
    """Create the final prompt based on the context and user input."""
    return f"{context}\n\nUser: {user_input}\nAssistant:"

def render_markdown(text: str) -> str:
    """Render Markdown into HTML."""
    return markdown2.markdown(text)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the homepage."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    """Handle the chat route and process user input."""
    try:
        data = await request.json()
        user_input = data["message"]

        context = select_relevant_context(user_input)
        prompt = create_prompt(context, user_input)

        response = ""
        for message in client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            stream=True,
        ):
            response += message.choices[0].delta.content
        
        formatted_response = render_markdown(response)

        return JSONResponse({"response": formatted_response})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

