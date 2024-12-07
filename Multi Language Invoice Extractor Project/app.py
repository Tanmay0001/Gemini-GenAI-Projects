from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Loading the updated Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initializing Streamlit app
st.set_page_config(page_title="Multiple Invoice Extractor")
st.header("Multiple Invoice Extractor")

input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Tell me about the invoice")  # Correct placement of submit button

    input_prompt = """
    You are an expert in understanding invoices. We will upload an image as an invoice 
    and you will have to answer any questions based on the uploaded image.
    """

    if submit:
        # Display a loading spinner
        with st.spinner("Processing your invoice..."):
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input, image_data, input_prompt)
        
        st.subheader("The Response is")
        st.write(response)
