import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.title("Web Content Q&A Tool")

# Fetch OpenAI API Key from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    # Initialize OpenAI and FAISS
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = None  # Initialize later after validating documents

    # Ingest URLs
    st.header("Ingest URLs")
    urls_input = st.text_area("Enter URLs:")
    if st.button("Ingest Content"):
        urls = [url.strip() for url in urls_input.split("\n") if url.strip()]
        if urls:
            documents = []
            for url in urls:
                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = ' '.join([p.get_text() for p in soup.find_all('p')]).strip()
                    if text:
                        doc = Document(page_content=text, metadata={"source": url})
                        documents.append(doc)
                    else:
                        st.warning(f"No textual content found at {url}.")
                except Exception as e:
                    st.error(f"Error ingesting {url}: {str(e)}")
            if documents:
                vector_store = FAISS.from_documents(documents, embeddings)
                st.success("Content ingested successfully.")
            else:
                st.error("No valid content ingested.")
        else:
            st.warning("Please enter a URL.")

    # Ask Questions
    st.header("Ask a Question")
    question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        if question:
            if not vector_store or not vector_store.index.ntotal:
                st.error("No content ingested. Please add URLs first.")
            else:
                qa_chain = RetrievalQA.from_chain_type(
                    llm=OpenAI(openai_api_key=openai_api_key),
                    chain_type="stuff",
                    retriever=vector_store.as_retriever()
                )
                answer = qa_chain.run(question)
                st.success(f"Answer: {answer}")
        else:
            st.warning("Please enter a question.")
else:
    st.error("OpenAI API key not found. Please set it")
