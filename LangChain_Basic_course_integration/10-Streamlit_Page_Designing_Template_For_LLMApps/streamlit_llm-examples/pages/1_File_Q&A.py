import streamlit as st
import anthropic

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
    "[原始碼連結](https://github.com/kevin801221/Langchain_course_code/blob/main/10-Streamlit_Page_Designing_Template_For_LLMApps/streamlit_llm-examples/pages/1_File_Q%26A.py)"

st.title("📝 File Q&A with Anthropic")
uploaded_file = st.file_uploader("'上傳一篇文章'", type=("txt", "md","pdf"))
question = st.text_input(
    "問問關於此上傳文章的問題吧!",
    placeholder="你可以給我一個簡短摘要嗎?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not anthropic_api_key:
    st.info("請給我你的Anthropic API KEY 然後才會繼續")

if uploaded_file and question and anthropic_api_key:
    article = uploaded_file.read().decode()
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",  # "claude-2" for Claude 2 model
        max_tokens_to_sample=100,
    )
    st.write("### Answer")
    st.write(response.completion)
