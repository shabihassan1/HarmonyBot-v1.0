# Harmony Bot V1.0

**Harmony Bot** is an intelligent conversational assistant built using Hugging Face's Inference API and the Meta LLaMA-3 model. It integrates mental health and medical counseling datasets to provide responses based on the user's input, offering tailored support for both general inquiries and health-related issues.

## Features

- **Conversational AI**: Powered by the Meta-Llama-3-8B-Instruct model to provide coherent and context-aware conversations.
- **Contextual Understanding**: Detects keywords related to mental health and medical inquiries to generate relevant and informed responses.
- **Rich Markdown Support**: Outputs are rendered using Markdown for better readability.
- **Hugging Face Integration**: Built using Hugging Face's Inference API for seamless integration with state-of-the-art NLP models.
- **FastAPI Framework**: Switched from Flask to FastAPI for better performance and modern async capabilities.
- **Deployed on Hugging Face Spaces**: The bot is hosted as a web app on Hugging Face Spaces, accessible directly through the space.

## Demo

Check out the live demo of the Harmony Bot here: [Harmony Bot on Hugging Face Spaces](https://huggingface.co/spaces/Shabi23/HarmonyBot)

## Project Structure

```bash
.
├── static/                   # Static files (background images, scripts, CSS)
├── templates/                # HTML templates for the front-end interface
├── application.py            # FastAPI application for backend logic
├── Dockerfile                # Docker configuration for deploying the app
├── README.md                 # Project documentation
├── Requirements.txt          # Python dependencies
└── .gitignore                # Git ignore configuration
```

## Requirements

- **Python 3.11 or above**
- **Hugging Face Hub Access**
- Datasets from Hugging Face: 
  - `avaliev/chat_doctor`
  - `Amod/mental_health_counseling_conversations`
- **FastAPI**, **uvicorn**
- **Markdown2** for rendering responses
- Other libraries as specified in `requirements.txt`

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/shabihassan1/HarmonyBot-v1.0.git

   ```
2. Navigate to the Project Directory:
   
   ```bash
    cd HarmonyBot-v1.0

   ```
3. Create and activate a virtual environment (optional but recommended):
    
   ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
   
   ```
   
4. Install the dependencies

   ```bash
    pip install -r Requirements.txt

   ```
5. Run the application:

   ```bash
    uvicorn application:app --host 0.0.0.0 --port 7680

    ```
6. Open your browser and go to http://127.0.0.1:7680 to access the web interface.


## Docker

You can also run the application in a Docker container:

1. Build the Docker image:

   ```bash
    docker build -t HarmonyBot-v1.0 .

   ```
2. Run the Docker container:

   ```bash
    docker run -p 8080:8080 HarmonyBot-v1.0
   
   ```

## Usage

After installation, open the application in your browser, and start chatting with HarmonyBot by asking questions related to either medical concerns or mental health.

**Example commands:**

- _"I’m feeling anxious. What should I do?"_
- _"What are the symptoms of the flu?"_

The bot will respond based on relevant datasets and models.

## How It Works

HarmonyBot uses two datasets:

- **avaliev/chat_doctor**: Focused on medical questions and answers between patients and doctors.
- **Amod/mental_health_counseling_conversations**: A mental health dataset to help guide users dealing with mental health challenges.

Upon receiving a user input, the bot:

1. Identifies the type of inquiry (mental health or medical) using keyword analysis.
2. Selects a relevant context from the dataset.
3. Uses this context to craft a prompt and generate a meaningful response via the **Meta-Llama-3-8B-Instruct** model.


## Technologies Used
- **FastAPI**: For creating the web application interface.
- **Hugging Face**: For model hosting and inference, using the **Meta-Llama 3-8B** model to generate AI responses. Hugging Face’s serverless API handles interactions with this model in a scalable, cost-efficient way.
- **Hugging Face Spaces**: A platform for hosting and sharing machine learning applications, using Docker for containerization, allowing the chatbot to run seamlessly on the web.
- **Docker**: To Containerize the application, ensuring that it runs consistently across different environments. Hugging Face Spaces leverages Docker to build and deploy the application in a fully isolated environment.
- **Uvicorn**: An ASGI server for asynchronous request handling, used with FastAPI to provide high-performance asynchronous processing.
- **Markdown2**: For rendering the AI-generated text into a readable HTML format.
- **Hugging Face Datasets**: The chatbot leverages two key datasets to answer medical and mental health-related queries.
**Languages Used**: Python (backend), JavaScript (frontend interactivity), HTML (structure), and CSS (styling).

## Group Members

This project was a collaborative effort by a group of passionate developers and AI enthusiasts. Meet the team behind HarmonyBot:

1. **Shabi ul Hassan**  
   [LinkedIn](https://www.linkedin.com/in/shabi-ul-hassan1/)  

2. **Abdullah Salman**  
   [LinkedIn](https://www.linkedin.com/in/abdullah-salman-89253b272/)  

3. **Nouman Hafeez**  
   [LinkedIn](https://www.linkedin.com/in/noumanhafeez11nh/)  

Together, we aimed to create a user-centric solution that leverages AI to improve access to medical and mental health advice. We are proud of this journey and excited about its potential impact!

We worked under the insightful supervision of **Dr. Mehreen Alam**, whose guidance and support were invaluable throughout the development process.  
   [LinkedIn](https://www.linkedin.com/in/dr-mehreen-alam-5a1b9720/)


## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for more details.

## Contributing

We welcome contributions to improve HarmonyBot! Please feel free to submit a pull request or open an issue on GitHub if you have any suggestions or improvements.


