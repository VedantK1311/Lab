import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to get response from OpenAI GPT model
def get_bot_response(user_input, context):
    # Join the context (last 5 prompts) into a single string for better conversation flow
    context_str = "\n".join(context)

    # Call OpenAI's completion API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" based on your needs
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": context_str},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150,
        temperature=0.7,
    )

    # Extract and return the bot's response
    bot_reply = response['choices'][0]['message']['content'].strip()
    return bot_reply

# Streamlit app
def main():
    # Set the title of the app
    st.title("Chatbot with OpenAI GPT (Last 5 Prompts Context)")

    # Instructions for the user
    st.write("Type something to start a conversation. The bot will consider the last 5 exchanges for context.")

    # Initialize chat history and context buffer (last 5 prompts)
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "context_buffer" not in st.session_state:
        st.session_state["context_buffer"] = []

    # Get user input
    user_input = st.text_input("You:", key="user_input")

    # If user submits input
    if user_input:
        # Append user input and bot response to chat history
        st.session_state["chat_history"].append(f"You: {user_input}")

        # Manage context buffer (only keep last 5 interactions)
        if len(st.session_state["context_buffer"]) >= 5:
            st.session_state["context_buffer"].pop(0)  # Remove oldest context entry
        st.session_state["context_buffer"].append(f"You: {user_input}")

        # Get the bot's response using OpenAI GPT
        bot_response = get_bot_response(user_input, st.session_state["context_buffer"])
        st.session_state["chat_history"].append(f"Bot: {bot_response}")

        # Append bot response to the context buffer as well
        st.session_state["context_buffer"].append(f"Bot: {bot_response}")

        # Clear the input field after submission
        st.session_state["user_input"] = ""

    # Display chat history
    for chat in st.session_state["chat_history"]:
        st.write(chat)

if __name__ == "__main__":
    main()
