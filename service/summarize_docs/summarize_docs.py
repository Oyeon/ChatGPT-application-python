import streamlit as st
from openai import OpenAI
from common.utils import load_config, load_prompt_template, get_gpt_response

# Load configuration and prompt template
config = load_config()
prompt_template = load_prompt_template()

##### Main function #####
def summarization_program():
    st.set_page_config(page_title="Summarization Program")
    
    initialize_session_state()
    client = display_sidebar()
    display_main_area(client)

def initialize_session_state():
    session_defaults = {
        'openai_api_key': '',
        'input_text': ''
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def display_sidebar():
    with st.sidebar:
        openai_api_key = st.text_input(label='OPENAI API Key', placeholder='Enter Your API Key', value=st.session_state['openai_api_key'], type='password')
        if openai_api_key:
            st.session_state['openai_api_key'] = openai_api_key
            client = OpenAI(api_key=openai_api_key)
        else:
            client = None
        st.markdown('---')
    return client

def display_main_area(client):
    st.header("📃 Summarization Program")
    st.markdown('---')
    
    selected_language = st.selectbox("Select language", config['languages'])
    input_text = st.text_area("Enter the text to summarize", value=st.session_state['input_text'])

    if st.button("Summarize"):
        generate_summary(client, selected_language, input_text)

def generate_summary(client, selected_language, input_text):
    st.session_state['input_text'] = input_text
    prompt = prompt_template.format(language=selected_language, text=input_text)
    st.info(get_gpt_response(client, prompt, config['openai_model']))

if __name__ == "__main__":
    summarization_program()