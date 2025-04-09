import streamlit as st
from bedrock_client import get_bedrock_client
import json

st.set_page_config(page_title="Claude Chat", page_icon="🤖")
st.title("🧠 Claude v2 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

client = get_bedrock_client()

def invoke_claude(prompt):
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": ["\n\nHuman:"]
    })

    response = client.invoke_model(
        body=body,
        modelId="anthropic.claude-v2",
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["completion"]

# Chat interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something to Claude...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            output = invoke_claude(user_input)
            st.markdown(output)
    st.session_state.messages.append({"role": "assistant", "content": output})
