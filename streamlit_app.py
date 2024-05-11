import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🦜🔗 Resumen de Texto")

# Replicate Credentials
with st.sidebar:
    st.title('🦜🔗 Resumen de Texto')
    st.write('Esta herramienta permite resumir textos con el modelo Llama 2 de Meta. Tenga en cuenta que ofrece un mayor rendimiento cuando el texto introducido está en inglés')

    replicate_api = st.secrets['REPLICATE_API_TOKEN']
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Elige modelo Llama2', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_summary(text_input):
    output = replicate.run(llm, 
                           input={"prompt": f"Please, reply only with a summary of the following text: '{text_input}'",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
   
    return output

# User-provided text
if text := st.text_area('Introduzca su texto:', disabled=not replicate_api):
    with st.spinner("Resumiendo...⏳"):
        summary = generate_llama2_summary(text)
        placeholder = st.empty()
        full_summary = ''
        for item in summary:
            full_summary += item
            placeholder.markdown(full_summary)
        placeholder.markdown(full_summary)


