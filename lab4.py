# Ensure pysqlite3 is used instead of the system sqlite3
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import openai
import fitz  # PyMuPDF for reading PDFs
import os

# Function to initialize the vector database and store in session state
def initialize_lab4_vectorDB(pdf_folder):
    # Check if the vectorDB already exists in session state
    if 'Lab4_vectorDB' not in st.session_state:
        # Create ChromaDB client and collection
        chroma_client = chromadb.Client()
        embedding_func = embedding_functions.OpenAIEmbeddingFunction(api_key="your_openai_api_key", model_name="text-embedding-ada-002")
        collection = chroma_client.create_collection(name="Lab4Collection", embedding_function=embedding_func)

        # Iterate over each PDF file in the folder
        for pdf_file in os.listdir(pdf_folder):
            if pdf_file.endswith('.pdf'):
                # Extract text from PDF
                pdf_text = extract_text_from_pdf(os.path.join(pdf_folder, pdf_file))
                
                # Create an embedding for the extracted text
                embedding = embedding_func([pdf_text])[0]

                # Add to ChromaDB collection with metadata (filename)
                collection.add(
                    documents=[pdf_text],
                    embeddings=[embedding],
                    metadatas=[{"filename": pdf_file}]
                )
        
        # Store the collection in Streamlit's session state to avoid re-initializing
        st.session_state.Lab4_vectorDB = collection

# Function to extract text from a PDF file using PyMuPDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to query the vector database
def query_vectorDB(query):
    # Make sure the vectorDB is initialized
    if 'Lab4_vectorDB' in st.session_state:
        # Perform a search
        results = st.session_state.Lab4_vectorDB.query(query_texts=[query], n_results=3)
        
        # Return the filenames of the top 3 results
        result_files = [result['metadata']['filename'] for result in results['metadatas'][0]]
        return result_files
    else:
        st.write("VectorDB is not initialized. Please initialize first.")

# Main Function to Run the Test
def run_test(pdf_folder, search_string):
    # Initialize the vector database
    initialize_lab4_vectorDB(pdf_folder)

    # Query the database with a test search string
    result_files = query_vectorDB(search_string)

    # Output the results (filenames of top 3 documents)
    st.write("Top 3 documents related to your query:")
    for i, filename in enumerate(result_files, 1):
        st.write(f"{i}. {filename}")

# Example usage (replace 'your_pdf_folder' with the actual folder path containing your PDFs)
# run_test('your_pdf_folder', "Generative AI")
