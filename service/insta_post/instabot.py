##### Basic Information #####
import streamlit as st
# Add OpenAI package
from openai import OpenAI
# Add Instagram package
from instagrapi import Client
# Image processing
from PIL import Image
import urllib
import json

from common.utils import load_config, load_prompt_template, get_gpt_response, get_gpt_image

config = load_config()

def upload_to_instagram(description):
    cl = Client()
    cl.login(st.session_state["instagram_ID"], st.session_state["instagram_Password"])
    cl.photo_upload("instaimg_resize.jpg", description)

def instabot():
    st.set_page_config(page_title="Instabot", page_icon="?")
    
    initialize_session_state()
    display_header()
    client = display_sidebar()
    handle_generate_button(client)
    handle_upload_section(client)

def initialize_session_state():
    session_defaults = {
        "description": "",
        "flag": False,
        "instagram_ID": "",
        "instagram_Password": "",
        "OPENAI_API": "",
        "openai_api_key": ""
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def display_header():
    st.header('Instagram Post Generator')
    st.markdown('---')
    with st.expander("Instagram Post Generator", expanded=True):
        st.write(
        """     
        - The Instagram post generator UI is created using Streamlit.
        - Images are generated using OpenAI's Dall.e 2.
        - Post text is generated using OpenAI's GPT model.
        - Automatic posting is done using the Instagram API.
        """
        )
        st.markdown("")

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

def handle_generate_button(client):
    topic = st.text_input(label="Topic", placeholder="Soccer, AI...")
    mood = st.text_input(label="Mood (e.g. funny, serious, sad)", placeholder="Funny")

    if st.button(label="Generate", type="secondary") and not st.session_state["flag"]:
        with st.spinner('Generating...'):
            generate_content(client, topic, mood)

def generate_content(client, topic, mood):
    prompt_template_TRANS = load_prompt_template('prompt_template_TRANS.txt')
    prompt = prompt_template_TRANS.format(topic=topic, mood=mood)
    output = get_gpt_response(client, prompt, config['openai_model'])

    output_data = json.loads(output)
    topic = output_data.get('topic', '')
    mood = output_data.get('mood', '')
    
    prompt_template_TEXT = load_prompt_template('prompt_template_TEXT.txt')            
    prompt = prompt_template_TEXT.format(topic=topic, mood=mood)
    st.session_state["description"] = get_gpt_response(client, prompt, config['openai_model'])

    prompt_template_IMAGE = load_prompt_template('prompt_template_IMAGE.txt')            
    prompt = prompt_template_IMAGE.format(topic=topic, mood=mood)
    url = get_gpt_image(client, prompt, config['dalle_model'])
    urllib.request.urlretrieve(url, "instaimg.jpg")

    st.session_state["flag"] = True

def handle_upload_section(client):
    if st.session_state["flag"]:
        image = Image.open('instaimg.jpg')  
        st.image(image)
        txt = st.text_area(label="Edit Description", value=st.session_state["description"], height=50)
        st.session_state["description"] = txt

        st.markdown('Instagram ID/Password')
        st.session_state["instagram_ID"] = st.text_input(label='ID', placeholder='Enter Your ID', value='')
        st.session_state["instagram_Password"] = st.text_input(label='Password', type='password', placeholder='Enter Your Password', value='')

        if st.button(label='Upload'):
            process_and_upload_image(client)

def process_and_upload_image(client):
    image = Image.open("instaimg.jpg")
    image = image.convert("RGB")
    new_image = image.resize((1080, 1080))
    new_image.save("instaimg_resize.jpg")
    upload_to_instagram(st.session_state["description"])
    st.session_state["flag"] = False

if __name__ == "__main__":
    instabot()