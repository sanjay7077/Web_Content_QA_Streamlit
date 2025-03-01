# Web_Content_QA_Streamlit
--------------------------

A Streamlit app that allows users to input URLs, ingest their content, and ask questions based on the scraped data using Langchain and OpenAI.

#Install Dependencies :-
------------------------

1.streamlit
2.langchain
3.langchain-community
4.requests
5.beautifulsoup
6.openai

#set your own openai_api_key

#Run the App
streamlit run web_content_qa_streamlit.py

#Tech Stack :
--------------
1.Frontend/UI: Streamlit
2.Backend/Q&A: Langchain + OpenAI
3.Embeddings & Vector Storage: OpenAI Embeddings + FAISS
4.Parsing: BeautifulSoup
5.Environment Management: dotenv

 #How It Works :
 ---------------
1️ Ingest URLs
User Input: Enter URLs into the text area.
Fetching Content:-
     Uses requests to fetch the HTML of each URL.
     Parses the page using BeautifulSoup to extract <p> tags (main content).
     If successful, wraps the text into Langchain Document objects.
Error Handling:
Alerts users if:-
    A URL is unreachable.
    The page has no textual content.
    The request fails or times out.
Vector Storage:-
    Valid documents are converted into embeddings using OpenAIEmbeddings.
    Stored in FAISS for efficient similarity search.

    
