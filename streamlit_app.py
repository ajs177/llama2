import streamlit as st
import replicate
import os

# Configuración de la página
st.set_page_config(page_title='🦙💬 Aplicación de Resumen de Texto')
st.title('🦙💬 Aplicación de Resumen de Texto')

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Text Summarizer')
    st.write('This text summarizer is created using the open-source Llama 2 LLM model from Meta.')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your text!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)

# Function for generating LLaMA2 response.
def generate_llama2_summary(text_input):
    output = replicate.run(llm, 
                           input={"prompt": f"Assistant: Please summarize the following text: '{text_input}'",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# Entrada de texto
txt_input = st.text_area('Introduce tu texto', '', height=200)

# Formulario para aceptar la entrada de texto del usuario para el resumen
result = []
with st.form('summarize_form', clear_on_submit=True):
    submitted = st.form_submit_button('Enviar')
    if submitted:
        with st.spinner('Calculando...'):
            summary = generate_llama2_summary(txt_input)
            result.append(summary)

# Muestra el resultado del resumen
if len(result):
    st.title('📝✅ Resultado del Resumen')
    st.info(result[0])

