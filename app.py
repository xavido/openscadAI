import streamlit as st
import speech_recognition as sr
from openai import OpenAI
import tempfile
import os

# Configuració de la pàgina
st.set_page_config(page_title="OpenSCAD Script Generator", layout="wide")

# Inicialitzar el client d'OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def transcribe_audio():
    # Inicialitzar el reconeixedor
    r = sr.Recognizer()
    
    # Gravar àudio del micròfon
    with sr.Microphone() as source:
        st.write("Parlant...")
        audio = r.listen(source)
        
    try:
        text = r.recognize_google(audio, language="ca-ES")
        return text
    except Exception as e:
        st.error(f"Error en la transcripció: {str(e)}")
        return None

def generate_openscad_script(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ets un expert en OpenSCAD. Genera codi OpenSCAD basant-te en les descripcions donades."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Interfície d'usuari
st.title("Generador de Scripts OpenSCAD")

# Columnes per organitzar la interfície
col1, col2 = st.columns([1, 1])

with col1:
    # Entrada de text
    prompt = st.text_area("Descriu el que vols crear:", height=100)
    
    # Botó per entrada de veu
    if st.button("🎤 Parla"):
        prompt = transcribe_audio()
        if prompt:
            st.write(f"Text transcrit: {prompt}")

    # Botó per generar
    if st.button("Genera Script"):
        if prompt:
            with st.spinner("Generant script..."):
                openscad_code = generate_openscad_script(prompt)
                st.session_state.openscad_code = openscad_code

with col2:
    # Mostrar el codi generat
    if 'openscad_code' in st.session_state:
        st.code(st.session_state.openscad_code, language='openscad')
        
        # Guardar i visualitzar el model
        if st.button("Visualitza"):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.scad') as tmp_file:
                tmp_file.write(st.session_state.openscad_code.encode())
                tmp_file_path = tmp_file.name
            
            # Aquí podries afegir la visualització utilitzant viewscad o una altra biblioteca
            st.write("Visualització no implementada encara") 