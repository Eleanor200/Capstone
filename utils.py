import openai

def get_initial_message():
    messages = [
        {"role": "system", "content": "You are now connected to our AI Banking Assistant. How can I assist you with your banking needs today?"},
        {"role": "user", "content": "What banking services do you offer?"},
        {"role": "assistant", "content": "I can provide information on account management, transactions, loans, and customer service issues. How may I assist you?"}
    ]
    return messages

def get_chatgpt_response(messages, model="gpt-4", domain="banking"):
    print("model: ", model)
    # Include a domain-specific prompt if necessary for future customization
    prompt = {
        "banking": "Please focus on providing banking-related support, including account management, transactions, loans, and customer service."
    }
    # Add the domain-specific instruction to the chat if applicable
    if domain in prompt:
        messages.append({"role": "system", "content": prompt[domain]})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=1024,  # Adjust max_tokens if needed
        temperature=0.7   # Adjust temperature to control creativity if needed
    )
    return response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

