from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure our API Key
genai.configure()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide SQL query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    # Combine the prompt and the question into a single string
    combined_input = prompt[0] + "\n" + question  # Combine prompt and question into one string
    response = model.generate_content([combined_input])  # Pass the combined input as a list
    return response.text

# Function to retrieve query from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define your prompt
prompt = [
    """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, MARKS

For example:
Example 1 - How many entries of records are present?
The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in Data Science class?
The SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science";

Also, the SQL code should not have ''' in the beginning or end, and the word "SQL" should not be in the output.
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)  # Get response from Gemini model
    st.subheader("Generated SQL Query:")
    st.code(response, language='sql')  # Display the generated SQL query
    
    # Execute the generated SQL query
    try:
        data = read_sql_query(response, "student.db")  # Pass the query to the database
        st.subheader("Query Results:")
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No results found.")
    except Exception as e:
        st.error(f"Error executing the SQL query: {e}")
