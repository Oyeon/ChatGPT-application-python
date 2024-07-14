import sys
import os
import streamlit as st
from openai import OpenAI
from common.utils import load_config, load_prompt_template, get_gpt_response

# Load configuration and prompt template
config = load_config()
prompt_template = load_prompt_template()

##### Main function #####
def ads_copywriter_program():
    st.set_page_config(page_title="Ad Copy Generator")

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

    # Main area
    st.header("🎸 Ad Copy Generator")
    st.markdown('---')

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name", placeholder=" ")
        product_features = st.text_input("Product Features", placeholder=" ")
        must_include_keywords = st.text_input("Must Include Keywords", placeholder=" ")
    with col2:
        brand_name = st.text_input("Brand Name", placeholder="Apple, Olive Young..")
        tone_and_manner = st.text_input("Tone and Manner", placeholder="Playful, Humorous, Emotional..")
        brand_core_value = st.text_input("Brand Core Value", placeholder="Enter if necessary")

    if st.button("Generate Ad Copy"):
        prompt = prompt_template.format(
            name=product_name,
            com_name=brand_name,
            value=brand_core_value,
            strength=product_features,
            tone_manner=tone_and_manner,
            keyword=must_include_keywords
        )
        st.info(get_gpt_response(client, prompt, config['openai_model']))

if __name__ == '__main__':
    ads_copywriter_program()