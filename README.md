# Coding-Assistant-using-Llama-3.2

This repository contains three implementations of a code assistant using the Ollama Llama 3.2 model running on a local machine. The assistant provides detailed, step-by-step guidance for writing code, troubleshooting errors, and solving coding-related queries across multiple programming languages and frameworks.

---

## Setup Ollama Llama 3.2

1. Ensure you have the **Ollama Llama 3.2 model** running on your local machine. The API should be accessible at:  
   `http://localhost:11434/api/generate`
2. Install the required Python packages:  
   ```bash
   pip install requests gradio tkinter pyinstaller
   ```
## 1. Gradio Chat Interface (code_assistant.py)
This implementation uses Gradio's ChatInterface to create a simple and fast LLM chat interface.

Code Explanation:
* The call_ollama_api function interacts with the Ollama API, incorporating the conversation history into the prompt.
* The chat_fn function handles the chat interaction, updating the history and returning the assistant's response.
* The Gradio interface is set up using gr.ChatInterface with context history enabled.

## 2. Gradio Custom Chatbot (code_assistant_modular.py)
This implementation uses Gradio's Chatbot function to create a customizable UI with additional buttons for retry, undo, and clear functionalities.

Code Explanation:
* The llama_chat function handles the chat interaction, updating the conversation history and user inputs.
* The retry_last, undo_last, and clear_chat functions provide additional functionalities for retrying, undoing, and clearing the chat.
* The Gradio interface is set up with custom buttons for retry, undo, and clear actions.

## 3. Tkinter Local UI (code_assistant_app.py)
This implementation uses the Tkinter library to create a local UI, which can be converted to a Windows executable file using PyInstaller.

Code Explanation:
* The llama_chat function handles the chat interaction, updating the conversation history and user inputs.
* The update_chat_display, on_send, on_retry, on_redo, and on_clear functions manage the UI interactions.
* The Tkinter UI is set up with a chat display area, input entry box, and action buttons for send, retry, redo, and clear actions.
##Converting to Executable
To convert the code_assistant_app.py script to a Windows executable file using PyInstaller, run the following command:
```bash
pyinstaller --onefile --windowed code_assistant_app.py
```
This will generate a dist folder containing the code_assistant_app.exe file.
### These three implementations provide different ways to interact with the Ollama Llama 3.2 model, each with its own advantages. Choose the one that best fits your needs.
