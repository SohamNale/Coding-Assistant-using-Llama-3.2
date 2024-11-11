import tkinter as tk
from tkinter import scrolledtext
import requests
import json

# Define the API URL
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Initialize history and user_inputs globally
history = []
user_inputs = []

# Function to handle API requests and manage chat history
def llama_chat(user_message, history, user_inputs):
    user_inputs.append(user_message)
    prompt = "You are a coding assistant. Provide detailed, step-by-step guidance for writing code, troubleshooting errors, and solving coding-related queries across multiple programming languages and frameworks. Respond concisely but with clarity, and ensure explanations are beginner-friendly where necessary, while also addressing more advanced questions.\n\n"
    
    # Build the prompt with all previous history
    for user_msg, assistant_msg in history:
        prompt += f"User: {user_msg}\n"
        if assistant_msg:
            prompt += f"Assistant: {assistant_msg}\n"
    
    # Add the latest user message to the prompt
    prompt += f"User: {user_message}\nAssistant:"

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            OLLAMA_API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        if response.status_code == 200:
            assistant_reply = response.json().get("response", "No response available.")
            history.append((user_message, assistant_reply))  # Append to history
            return history, user_inputs, ""
        else:
            return history, user_inputs, f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return history, user_inputs, f"Request failed: {str(e)}"

def update_chat_display():
    chat_display.config(state="normal")
    chat_display.delete("1.0", tk.END)
    for user_msg, assistant_msg in history:
        chat_display.insert(tk.END, f"{user_msg}\n", "user")
        chat_display.insert(tk.END, "\n", "blank")
        chat_display.insert(tk.END, f"{assistant_msg}\n\n", "assistant")
        chat_display.insert(tk.END, "\n", "blank")
    chat_display.config(state="disabled")

def on_send():
    global history, user_inputs
    user_message = input_entry.get()
    if user_message:
        history, user_inputs, _ = llama_chat(user_message, history, user_inputs)
        update_chat_display()
        input_entry.delete(0, tk.END)

def on_retry():
    global history, user_inputs
    if user_inputs:
        last_input = user_inputs[-1]
        history, user_inputs, _ = llama_chat(last_input, history[:-1], user_inputs)  # Retry without last history item
        update_chat_display()
        # Do not set the input entry text to the last input on retry
        input_entry.delete(0, tk.END)

def on_redo():
    global history, user_inputs
    if user_inputs:
        last_input = user_inputs.pop()
        if history:
            history.pop()  # Remove last history entry
        update_chat_display()
        input_entry.delete(0, tk.END)
        input_entry.insert(0, last_input)

def on_clear():
    global history, user_inputs
    history.clear()
    user_inputs.clear()
    update_chat_display()

# Initialize Tkinter UI
root = tk.Tk()
root.title("Chat Assistant")
root.configure(bg="black")

# Create a display area for chat history
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=30, width=70, bg="black", fg="white", state="disabled", font=("Arial", 12))
chat_display.tag_configure("user", background="#444444", foreground="white", font=("Arial", 12), relief="solid", borderwidth=1)
chat_display.tag_configure("assistant", background="#555555", foreground="white", font=("Arial", 12), relief="solid", borderwidth=1)
chat_display.tag_configure("blank", background="black")
chat_display.pack(pady=10, padx=10)

# Input frame for the entry box and send button
input_frame = tk.Frame(root, bg="black")
input_frame.pack(pady=10, padx=10)

# Create an input entry box for messages
input_entry = tk.Entry(input_frame, font=("Arial", 12), width=40, bg="#333333", fg="white", relief="solid", bd=0, insertbackground="white")
input_entry.config(highlightbackground="#333333", highlightcolor="#333333", highlightthickness=2)
input_entry.pack(side="left", padx=5)

# Bind Enter key to the send action
root.bind('<Return>', lambda event: on_send())

# Create a send button next to the input box
send_button = tk.Button(input_frame, text="Send", command=on_send, bg="#333333", fg="white", relief="solid", bd=0, font=("Arial", 10), padx=10, pady=5)
send_button.config(highlightbackground="#333333", highlightcolor="#333333", highlightthickness=2)
send_button.pack(side="right", padx=5)

# Action buttons (Retry, Redo, Clear) below the input
action_frame = tk.Frame(root, bg="black")
action_frame.pack(pady=10)

retry_button = tk.Button(action_frame, text="Retry", command=on_retry, bg="#333333", fg="white", relief="solid", bd=0, font=("Arial", 10), padx=10, pady=5)
retry_button.config(highlightbackground="#333333", highlightcolor="#333333", highlightthickness=2)
retry_button.pack(side="left", padx=5)

redo_button = tk.Button(action_frame, text="Redo", command=on_redo, bg="#333333", fg="white", relief="solid", bd=0, font=("Arial", 10), padx=10, pady=5)
redo_button.config(highlightbackground="#333333", highlightcolor="#333333", highlightthickness=2)
redo_button.pack(side="left", padx=5)

clear_button = tk.Button(action_frame, text="Clear", command=on_clear, bg="#333333", fg="white", relief="solid", bd=0, font=("Arial", 10), padx=10, pady=5)
clear_button.config(highlightbackground="#333333", highlightcolor="#333333", highlightthickness=2)
clear_button.pack(side="left", padx=5)

# Run the Tkinter main loop
root.mainloop()
