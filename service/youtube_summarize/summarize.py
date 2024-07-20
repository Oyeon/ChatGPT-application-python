##### Basic Information #####
import streamlit as st
# Added for URL analysis
import re
# Added Langchain package
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
# Added for translation
from googletrans import Translator

##### Function Implementation #####
# English Translation
def google_trans(messages):
    google = Translator()
    result = google.translate(messages, dest="ko")

    return result.text

# Youtube URL Check
def youtube_url_check(url):
    pattern = r'^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)(\&ab_channel=[\w\d]+)?$'
    match = re.match(pattern, url)
    return match is not None

##### Main Function #####
def main():

    # Basic Settings
    st.set_page_config(page_title="YouTube Summarize", layout="wide")

    # Initialize session state
    if "flag" not in st.session_state:
        st.session_state["flag"] = True
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
    if "summarize" not in st.session_state:
        st.session_state["summarize"] = ""

    # Title
    st.header(" 📹English YouTube Content Summarizer/Script Translator")
    st.markdown('---')
    # Get URL input
    st.subheader("Enter YouTube URL")
    youtube_video_url = st.text_input("  ", placeholder="https://www.youtube.com/watch?v=**********")

    # Create sidebar
    with st.sidebar:
        # Get Open AI API key input
        open_apikey = st.text_input(label='OPENAI API Key', placeholder='Enter Your API Key', value='', type='password')
        
        # Display the input API key
        if open_apikey:
            st.session_state["OPENAI_API"] = open_apikey 
        st.markdown('---')

    if len(youtube_video_url) > 2:
        if not youtube_url_check(youtube_video_url):
            st.error("Please check the YouTube URL.")
        else:

            width = 50
            side = width / 2
            _, container, _ = st.columns([side, width, side])
            # Show the input YouTube video
            container.video(data=youtube_video_url)
            
            # Extract script
            loader = YoutubeLoader.from_youtube_url(youtube_video_url)
            transcript = loader.load()
        
            st.subheader("Summary Result")
            if st.session_state["flag"]:
                # Set LLM model
                llm = ChatOpenAI(temperature=0,
                        openai_api_key=st.session_state["OPENAI_API"],
                        max_tokens=3000,
                        model_name="gpt-3.5-turbo",
                        request_timeout=120
                    )
                
                # Set summary prompt
                prompt = PromptTemplate(
                    template="""Summarize the youtube video whose transcript is provided within backticks \
                    ```{text}```
                    """, input_variables=["text"]
                )
                combine_prompt = PromptTemplate(
                    template="""Combine all the youtube video transcripts provided within backticks \
                    ```{text}```
                    Provide a concise summary between 8 to 10 sentences.
                    """, input_variables=["text"]
                )

                # Split script
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
                text = text_splitter.split_documents(transcript)

                # Execute summary
                chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False,
                                                map_prompt=prompt, combine_prompt=combine_prompt)
                st.session_state["summarize"] = chain.run(text)
                st.session_state["flag"] = False
            st.success(st.session_state["summarize"])
            # Translate   
            transe = google_trans(st.session_state["summarize"])
            st.subheader("Summary Translation Result")
            st.info(transe)
            
            # Translate script
            st.subheader("Translate Script")  
            if st.button("Execute Script Translation"):
                transe = google_trans(transcript[0])
                st.markdown(transe)

if __name__ == "__main__":
    main() 
