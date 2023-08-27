import os
import streamlit as st
import requests
import openai

# Streamlit UI
tab0, tab1 = st.tabs(["Home", "Chatbot"])

with st.sidebar:
    st.header("Configuración de clave")
    openai_api_key = st.sidebar.text_input("Clave que recibiste", type="password")
    if openai_api_key is not None and openai_api_key != '':
        st.success('Gracias, recibimos tu clave', icon="✅")

with tab0:
    st.header("Bienvenido a Copilot 🤖")
    st.info("No olvides ingresar la clave en el menú desplegable de la izquierda.\
            Luego, Selecciona alguna de las pestañas para comenzar a utilizar la herramienta.")

with tab1:
    st.header("Interactua con el asistente a través del chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []

if tab1:
    st.info("Nota: El asistente no sustituye la opinión de un médico. Te recomendamos consultar con un profesional de la salud.")
    openai.api_key = openai_api_key
    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                 st.markdown(message["content"])

    if prompt := st.chat_input("haz una pregunta"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
             st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            messages_list = [
                {"role": "system", "content": "Tu nombre es Alfred.Eres un asistente especializado en brindar sugerencias\
                                                médicas relacionadas con temas cardiológicos. Solo puedes comunicarte en español."}
            ]
            messages_list += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages_list, stream=True):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})