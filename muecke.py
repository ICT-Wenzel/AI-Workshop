import streamlit as st
import requests
from requests.exceptions import RequestException
# Seiteneinstellungen
st.set_page_config(page_title='Chat', layout='centered')

# Webhook URL
WEBHOOK_URL = st.secrets.get("WEBHOOK_URL", None)   


# Titel
st.title('🤖 Chat')

# Chat-Historie initialisieren
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Chat-Historie anzeigen
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Chat-Input
if prompt := st.chat_input('Nachricht eingeben...'):
    # User-Nachricht hinzufügen
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.write(prompt)
    
    # Bot-Antwort
    with st.chat_message('assistant'):
        with st.spinner('Antwort wird generiert...'):
            try:
                payload = {'message': prompt}
                response = requests.post(
                    WEBHOOK_URL, 
                    json=payload, 
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                bot_response = response.json().get('response', response.text)
                st.write(bot_response)
                st.session_state.messages.append({'role': 'assistant', 'content': bot_response})
            except Exception as e:
                error_msg = f'Fehler: {str(e)}'
                st.error(error_msg)
                st.session_state.messages.append({'role': 'assistant', 'content': error_msg})