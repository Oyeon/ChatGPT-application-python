import streamlit as st
import re
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from openai import OpenAI
from common.utils import load_config, load_prompt_template, get_gpt_response, get_gpt_image

config = load_config()

def youtube_url_check(url):
    pattern = r'^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)(\&ab_channel=[\w\d]+)?$'
    match = re.match(pattern, url)
    return match is not None

def initialize_session_state():
    if "flag" not in st.session_state:
        st.session_state["flag"] = True
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
    if "summarize" not in st.session_state:
        st.session_state["summarize"] = ""

def get_youtube_url_input():
    st.subheader("Enter YouTube URL")
    return st.text_input("  ", placeholder="https://www.youtube.com/watch?v=**********")

def display_video(youtube_video_url):
    width = 50
    side = width / 2
    _, container, _ = st.columns([side, width, side])
    container.video(data=youtube_video_url)

def extract_transcript(youtube_video_url):
    loader = YoutubeLoader.from_youtube_url(youtube_video_url)
    return loader.load()

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

def langchain_summarize(transcript):
    # Set LLM model
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=st.session_state["OPENAI_API"],
        max_tokens=3000,
        model_name="gpt-3.5-turbo",
        request_timeout=120
    )
    
    prompt_template_SUMMARIZE = load_prompt_template('chunk_summarize.txt')
    prompt_template_COMBINE = load_prompt_template('all_summarize.txt')
    prompt = PromptTemplate(
        template=prompt_template_SUMMARIZE, 
        input_variables=["text"]
    )
    combine_prompt = PromptTemplate(
        template=prompt_template_COMBINE, 
        input_variables=["text"]
    )                
    # Split script
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
    text = text_splitter.split_documents(transcript)

    # Execute summary
    chain = load_summarize_chain(
        llm, 
        chain_type="map_reduce", 
        verbose=False,
        map_prompt=prompt, 
        combine_prompt=combine_prompt
    )
    st.session_state["summarize"] = chain.run(text)
    st.session_state["flag"] = False

def youtube_summarize():
    st.set_page_config(page_title="YouTube Summarize", layout="wide")
    initialize_session_state()
    
    st.header(" 📹English YouTube Content Summarizer/Script Translator")
    st.markdown('---')

    youtube_video_url = get_youtube_url_input()
    client = create_sidebar()

    if len(youtube_video_url) > 2:
        if not youtube_url_check(youtube_video_url):
            st.error("Please check the YouTube URL.")
        else:
            display_video(youtube_video_url)
            if st.button("You want to get Transcript from Youtube and Translate with it?"):
                transcript = extract_transcript(youtube_video_url)
                st.subheader("Summary Result")
                if st.session_state["flag"]:
                    langchain_summarize(transcript)
                st.success(st.session_state["summarize"])
                translate_summary(client)

if __name__ == "__main__":
    youtube_summarize() 
