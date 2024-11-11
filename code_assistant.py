import requests
import json
import gradio as gr

# Define the function to interact with the Ollama API, now incorporating history
def call_ollama_api(user_message, history):
    url = "http://localhost:11434/api/generate"  # Ollama API endpoint

    # Generate the conversation history prompt
    context_prompt = "You are a coding assistant. Provide detailed, step-by-step guidance for writing code, troubleshooting errors, and solving coding-related queries across multiple programming languages and frameworks. Respond concisely but with clarity, and ensure explanations are beginner-friendly where necessary, while also addressing more advanced questions.\n\n"

    # Compile history into the context for the prompt
    for message in history:
        role = "User" if message["role"] == "user" else "Assistant"
        context_prompt += f"{role}: {message['content']}\n"
    
    # Add the latest user message
    context_prompt += f"User: {user_message}\nAssistant:"

    # Define the payload for the Ollama API
    data = {
        "model": "llama3.2",  # Specify your model name
        "prompt": context_prompt,
        "stream": False,      # Disable streaming for simplicity
        "temperature": 0.7,   # Control randomness
        "max_tokens": 500,    # Maximum tokens in response
        "top_p": 0.9          # Nucleus sampling
    }
    
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("response", "No response available from the model.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama API: {e}"

# Chat function with updated history handling
def chat_fn(user_message, history):
    # Get response from the Ollama API
    response = call_ollama_api(user_message, history)
    
    # Append user message and assistant response to the history
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": response})
    
    # Return updated history and response
    return response

# Set up the Gradio interface using gr.ChatInterface with context history enabled
chat_interface = gr.ChatInterface(
    fn=chat_fn,
    type="messages",
    title="Code Assistant",
    description="Interact with the assistant to get help with code, solve errors, and get clear explanations based on conversation history."
)

# Launch the Gradio app
chat_interface.launch()
