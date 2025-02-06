import streamlit as st

from image_store import ImageStore

st.title("Reverse Image Search")

uploaded_file = st.file_uploader(
    "Choose an image",
    accept_multiple_files=False,
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    retrieved_docs = ImageStore.retrieve_docs_by_image(uploaded_file)

    for doc in retrieved_docs:
        st.image(ImageStore.get_image_path_by_id(doc.id), caption=doc.page_content)