import streamlit as st
from openai import OpenAI
from common.utils import load_config, load_prompt_template, get_gpt_response

# Load configuration and prompt template
config = load_config()
prompt_template = load_prompt_template()

##### Main function #####
def summarization_program():
    st.set_page_config(page_title="Summarization Program")
    
    # Initialize session state
    if 'openai_api_key' not in st.session_state:
        st.session_state['openai_api_key'] = ''
    if 'input_text' not in st.session_state:
        st.session_state['input_text'] = ''

    # Sidebar
    with st.sidebar:
        # Input Open AI API key
        openai_api_key = st.text_input(label='OPENAI API Key', placeholder='Enter Your API Key', value=st.session_state['openai_api_key'], type='password')    
        # Display the input API key
        if openai_api_key:
            st.session_state['openai_api_key'] = openai_api_key
            client = OpenAI(api_key=openai_api_key)
        st.markdown('---')

    st.header("📃 Summarization Program")
    st.markdown('---')
    
    selected_language = st.selectbox("Select language", config['languages'])
    input_text = st.text_area("Enter the text to summarize", value=st.session_state['input_text'])

    if st.button("Summarize"):
        st.session_state['input_text'] = input_text
        prompt = prompt_template.format(language=selected_language, text=input_text)
        st.info(get_gpt_response(client, prompt, config['openai_model']))

if __name__ == "__main__":
    summarization_program()