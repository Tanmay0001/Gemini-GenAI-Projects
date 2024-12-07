from dotenv import load_dotenv
load_dotenv()  # loading all environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")  # Gemini Pro is used for text data

def get_gemini_response(question):
    response = model.generate_content(question)  # Capture the response from generate_content
    # Extract the text content from the response object
    if response and response.candidates:
        text_content = response.candidates[0].content.parts[0].text
        return text_content
    return "No response generated."

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# When submit is clicked
if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)
