from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

load_dotenv()  # Loading all environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Setting up API key

# Function to load the new gemini 1.5 flash model and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Switching to new model
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Streamlit app initialization
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")

# User input and file upload
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# # Nutrition prompt
# input_prompt = """
# You are an expert nutritionist. Please analyze the food items in the uploaded image 
# and calculate the total calories. Provide the details of each item with its calorie intake in the format:

# 1. Item 1 - X calories
# 2. Item 2 - Y calories
# ...
# """


input_prompt = """
You are an expert nutritionist. Please analyze the food items in the uploaded image 
and estimate the total calories based on common portion sizes and ingredients. 
If exact calorie counts aren't possible, provide an approximation with details for each item.
If you can't recognize an item, please mention it in the response.

Provide the details in the following format:

1. Item 1 - Estimated calories
2. Item 2 - Estimated calories
...
"""


submit = st.button("Tell me about the total calories")

# If submit button is clicked
if submit:
    if uploaded_file is not None:
        # Calling the function with correct arguments
        responses = get_gemini_response(input_text, [image], input_prompt)
        st.subheader("The Response is ")
        st.write(responses)  # Display the response from Gemini
    else:
        st.warning("Please upload an image first.")
