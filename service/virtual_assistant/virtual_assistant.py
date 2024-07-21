##### Basic Information Input #####
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import os
from datetime import datetime
from gtts import gTTS
import base64

##### Function Implementation #####
def speech_to_text(audio, apikey):
    filename = 'input.mp3'
    with open(filename, "wb") as f:
        f.write(audio)
    with open(filename, "rb") as audio_file:
        client = openai.OpenAI(api_key=apikey)
        response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        transcript = response.text
    os.remove(filename)
    return transcript

def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key=apikey)
    response = client.chat.completions.create(model=model, messages=prompt)
    return response.choices[0].message.content

def text_to_speech(response):
    filename = "output.mp3"
    tts = gTTS(text=response, lang="ko")
    tts.save(filename)
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="True">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    os.remove(filename)

def initialize_session_state():
    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean"}]
    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

def display_header():
    st.header("Voice Assistant Program")
    st.markdown("---")
    with st.expander("About the Voice Assistant Program", expanded=True):
        st.write(
            """     
            - The UI of the voice assistant program was created using Streamlit.
            - STT (Speech-To-Text) uses OpenAI's Whisper AI.
            - Responses are generated using OpenAI's GPT model.
            - TTS (Text-To-Speech) uses Google's Google Translate TTS.
            """
        )
        st.markdown("")

def display_sidebar():
    with st.sidebar:
        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API Key", placeholder="Enter Your API Key", value="", type="password")
        st.markdown("---")
        model = st.radio(label="GPT Model", options=["gpt-4", "gpt-3.5-turbo"])
        st.markdown("---")
        if st.button(label="Reset"):
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean"}]
            st.session_state["check_reset"] = True
    return model

def handle_audio_input():
    audio = audio_recorder("Click to Record", "Recording...")
    if audio is not None:
        st.audio(audio)
        question = speech_to_text(audio, st.session_state["OPENAI_API"])
        now = datetime.now().strftime("%H:%M")
        st.session_state["chat"] = st.session_state["chat"] + [("user", now, question)]
        st.session_state["messages"] = st.session_state["messages"] + [{"role": "user", "content": question}]
        return question
    return None

def handle_response(model):
    response = ask_gpt(st.session_state["messages"], model, st.session_state["OPENAI_API"])
    st.session_state["messages"] = st.session_state["messages"] + [{"role": "system", "content": response}]
    now = datetime.now().strftime("%H:%M")
    st.session_state["chat"] = st.session_state["chat"] + [("bot", now, response)]
    for sender, time, message in st.session_state["chat"]:
        if sender == "user":
            st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
            st.write("")
        else:
            st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
            st.write("")
    text_to_speech(response)

##### Main Function #####
def virtual_assistant():
    st.set_page_config(page_title="Voice Assistant Program", layout="wide")
    initialize_session_state()
    display_header()
    model = display_sidebar()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ask a Question")
        question = handle_audio_input()
    with col2:
        st.subheader("Question/Answer")
        if question is not None:
            handle_response(model)
        else:
            st.session_state["check_reset"] = False

if __name__ == "__main__":
    virtual_assistant()