import streamlit as st
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
WOLFRAM_ALPHA_APPID = os.getenv("WOLFRAM_ALPHA_APPID")

def get_full_results(query):
    base_url = "http://api.wolframalpha.com/v2/query"
    encoded_query = quote(query)
    url = f"{base_url}?appid={WOLFRAM_ALPHA_APPID}&input={encoded_query}&format=plaintext"

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_xml_results(xml_string):
    root = ET.fromstring(xml_string)
    results = []
    for pod in root.findall('.//pod'):
        pod_title = pod.get('title')
        pod_content = []
        for subpod in pod.findall('.//subpod'):
            plaintext = subpod.find('plaintext')
            if plaintext is not None and plaintext.text:
                pod_content.append(plaintext.text.strip())
        if pod_content:
            results.append((pod_title, pod_content))
    return results

def full_results_api_content():
    st.title("Wolfram Alpha Full Results API")

    query = st.text_input("Enter your query:")

    if st.button("Get Full Results"):
        if query:
            xml_results = get_full_results(query)
            if xml_results:
                parsed_results = parse_xml_results(xml_results)
                for title, content in parsed_results:
                    st.subheader(title)
                    for item in content:
                        st.write(item)
                        st.write("---")
            else:
                st.error("Failed to retrieve results from Wolfram Alpha.")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    full_results_api_content()