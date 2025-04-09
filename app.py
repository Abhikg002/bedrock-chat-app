import streamlit as st
import boto3
import json

st.set_page_config(page_title="Claude Chat", page_icon="🤖")
st.title("🧠 Claude v2 Chat (Bring Your Own AWS Keys)")

# Step 1: Ask for AWS keys from user
with st.sidebar:
    st.header("🔐 AWS Credentials")
    aws_access_key_id = st.text_input("Access Key ID", type="password")
    aws_secret_access_key = st.text_input("Secret Access Key", type="password")
    aws_region = st.text_input("AWS Region", value="us-east-1")

# Step 2: Check if keys are provided
if not (aws_access_key_id and aws_secret_access_key and aws_region):
    st.warning("Please enter your AWS credentials in the sidebar.")
    st.stop()

# Step 3: Create Bedrock client
def get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

client = get_bedrock_client()

# Step 4: Chat app logic
if "messages" not in st.session_state:
    st.session_state.messages = []

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

# Display chat
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
