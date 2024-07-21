##### Basic Information Input #####
import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from openai import OpenAI
from common.utils import load_config, load_prompt_template, get_gpt_response

config = load_config()

def create_sidebar():
    with st.sidebar:
        openai_api_key = st.text_input(label='OPENAI API Key', placeholder='Enter Your API Key', value='', type='password')
        if openai_api_key:
            st.session_state["OPENAI_API"] = openai_api_key 
            client = OpenAI(api_key=openai_api_key)
        else:
            client = None
        st.markdown('---')
    return client

def translate_summary(client):
    prompt_template_TRANS = load_prompt_template('prompt_template_TRANS.txt')
    prompt = prompt_template_TRANS.format(text=st.session_state["summarize"], language="Korean")
    transe = get_gpt_response(client, prompt, config['openai_model'])
    st.subheader("Summary Translation Result")
    st.info(transe)

def pdf_splliter_func(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    cleaned_chunks = [chunk.replace('<|endofprompt|>', '') for chunk in chunks]
    return cleaned_chunks

def QA_question(client, cleaned_chunks, user_question):
    embeddings = OpenAIEmbeddings(openai_api_key=st.session_state["OPENAI_API"])
    knowledge_base = FAISS.from_texts(cleaned_chunks, embeddings)
    docs = knowledge_base.similarity_search(user_question)

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=st.session_state["OPENAI_API"],
        max_tokens=2000,
        model_name='gpt-3.5-turbo',
        request_timeout=120
    )
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=docs, question=user_question)
    return response

##### Main Function #####
def summarize_pdf():
    st.set_page_config(page_title="PDF Analyzer", layout="wide")
    client = create_sidebar()
        
    st.header("PDF Content Question Program📜")
    st.markdown('---')
    st.subheader("Upload your PDF file")
    pdf = st.file_uploader(" ", type="pdf")
    if pdf is not None:
        cleaned_chunks = pdf_splliter_func(pdf)
        st.markdown('---')
        st.subheader("Enter your question")
        user_question = st.text_input("Ask a question about your PDF:")
        if user_question:
            response = QA_question(client, cleaned_chunks, user_question)
            st.info(response)
            if st.button(label="Translate"):
                st.session_state["summarize"] = response
                translate_summary(client)

if __name__=='__main__':
    summarize_pdf()