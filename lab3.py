import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to get response from OpenAI GPT model (using new API)
def get_bot_response(user_input, context):
    # Join the context (last 5 prompts) into a single string for better conversation flow
    context_str = "\n".join(context)
    prompt = f"{context_str}\nYou: {user_input}\nBot:"

    # Call OpenAI's completion API (using the newer syntax with prompt)
    response = openai.Completion.create(
        model="gpt-4",  # Adjust this to "gpt-3.5-turbo" or "davinci" based on availability
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=["You:", "Bot:"]
    )

    # Extract and return the bot's response
    bot_reply = response.choices[0].text.strip()
    return bot_reply

# Streamlit app
def main():
    st.title("Chatbot with OpenAI GPT (Last 5 Prompts Context)")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "context_buffer" not in st.session_state:
        st.session_state["context_buffer"] = []

    user_input = st.text_input("You:", key="user_input")

    if user_input:
        st.session_state["chat_history"].append(f"You: {user_input}")

        if len(st.session_state["context_buffer"]) >= 5:
            st.session_state["context_buffer"].pop(0)
        st.session_state["context_buffer"].append(f"You: {user_input}")

        bot_response = get_bot_response(user_input, st.session_state["context_buffer"])
        st.session_state["chat_history"].append(f"Bot: {bot_response}")

        st.session_state["context_buffer"].append(f"Bot: {bot_response}")
        st.session_state["user_input"] = ""

    for chat in st.session_state["chat_history"]:
        st.write(chat)

if __name__ == "__main__":
    main()
