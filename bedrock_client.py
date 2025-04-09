import boto3
import streamlit as st

def get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=st.secrets["aws_region"],
        aws_access_key_id=st.secrets["aws_access_key_id"],
        aws_secret_access_key=st.secrets["aws_secret_access_key"]
    )
