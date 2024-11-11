import gradio as gr
import requests
import json

# Define the Ollama API URL
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Function to interact with the Ollama API
def llama_chat(user_message, history, user_inputs):
    """
    Handles the chat interaction between the user and Llama 3.1 via Ollama API.

    Parameters:
    - user_message (str): The latest message from the user.
    - history (list): List of previous (user, assistant) messages.
    - user_inputs (list): List of user inputs to enable undo functionality.

    Returns:
    - history (list): Updated conversation history with the assistant's response.
    - user_inputs (list): Updated user input list.
    """
    history = history or []
    user_inputs.append(user_message)  # Store only user message in user_inputs

    # Append user message to conversation history
    history.append((user_message, None))  # Add user message with None as placeholder for assistant reply

    # Combine the conversation history into a single prompt with system instructions
    prompt = "You are a coding assistant. Provide detailed, step-by-step guidance for writing code, troubleshooting errors, and solving coding-related queries across multiple programming languages and frameworks. Respond concisely but with clarity, and ensure explanations are beginner-friendly where necessary, while also addressing more advanced questions.\n\n"
    for user_msg, assistant_msg in history:
        prompt += f"User: {user_msg}\n"
        if assistant_msg:
            prompt += f"Assistant: {assistant_msg}\n"

    # Define the payload for the Ollama API
    payload = {
        "model": "llama3.1",  # Specify your model name
        "prompt": prompt,
        "stream": False,      # Disable streaming for simplicity
        "temperature": 0.7,   # Control randomness
        "max_tokens": 500,    # Maximum tokens in response
        "top_p": 0.9          # Nucleus sampling
    }

    try:
        # Make the POST request to Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            response_data = response.json()
            assistant_reply = response_data.get("response", "No response available.")

            # Append assistant's reply to the conversation history
            history[-1] = (user_message, assistant_reply)

            return history, user_inputs, ""  # Clear the input box for the next input
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            history[-1] = (user_message, error_message)  # Update the latest message with the error
            return history, user_inputs, ""  # Clear the input box

    except requests.exceptions.RequestException as e:
        error_message = f"Request failed: {str(e)}"
        history[-1] = (user_message, error_message)  # Update the latest message with the error
        return history, user_inputs, ""  # Clear the input box

# Retry functionality to regenerate the last response
def retry_last(history, user_inputs):
    if user_inputs:
        last_user_message = user_inputs[-1]  # Get the last user message
        return llama_chat(last_user_message, history[:-1], user_inputs)  # Regenerate response for the last message
    return history, user_inputs, ""  # Reset the input box

# Undo functionality to allow user to edit last input
def undo_last(history, user_inputs):
    if user_inputs:
        last_user_message = user_inputs.pop()  # Get the last user message
        return history[:-1], user_inputs, last_user_message  # Remove the last conversation from history and return it in the text box
    return history, user_inputs, ""  # Reset if no history

# Function to clear the conversation history
def clear_chat():
    return [], [], "", []  # Clear chatbot history, message textbox, and user inputs

# Define the Gradio Chat Interface
with gr.Blocks() as demo:
    gr.Markdown("<h1><center>Code Assistant</center></h1>")
    gr.Markdown("Interact with the assistant to get help with code, solve errors, and get clear explanations based on conversation history.")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(
        placeholder="Enter your message here...",
        label="Your Message"
    )
    # Buttons: Retry, Undo, and Clear, all aligned horizontally
    with gr.Row():
        retry_btn = gr.Button("Retry")
        undo_btn = gr.Button("Undo")
        clear_btn = gr.Button("Clear")

    # Define the interactions
    user_inputs = gr.State([])  # Separate state to store only user inputs
    msg.submit(llama_chat, [msg, chatbot, user_inputs], [chatbot, user_inputs, msg])
    retry_btn.click(retry_last, [chatbot, user_inputs], [chatbot, user_inputs, msg])
    undo_btn.click(undo_last, [chatbot, user_inputs], [chatbot, user_inputs, msg])  # Return the last input to the text box for editing
    clear_btn.click(clear_chat, [], [chatbot, chatbot, msg, user_inputs])

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()