import streamlit as st

from image_store import ImageStore

st.title("Image Search")

query = st.text_input("Enter query:")

if query:
    retrieved_docs = ImageStore.retrieve_docs_by_query(query)

    for doc in retrieved_docs:
        st.image(ImageStore.get_image_path_by_id(doc.id), caption=doc.page_content)