import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = 'your-api-key'

def get_response(message):
    response = openai.Completion.create(
      engine="text-davinci-003",  # Choose a model
      prompt=message,
      max_tokens=150
    )
    return response.choices[0].text.strip()

st.title('Simple Chatbot')

user_input = st.text_input("Talk to the chatbot:")

if user_input:
    chatbot_response = get_response(user_input)
    st.text_area("Chatbot says:", value=chatbot_response, height=200, max_chars=None, key=None)
