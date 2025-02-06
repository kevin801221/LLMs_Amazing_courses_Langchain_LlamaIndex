import streamlit as st

from image_store import ImageStore

st.title("Upload Images")

uploaded_files = st.file_uploader(
    "Choose an image",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png"]
)

for uploaded_file in uploaded_files:
    doc_id = ImageStore.upload_image(uploaded_file)
    st.image(ImageStore.get_image_path_by_id(doc_id), caption=ImageStore.get_by_id(doc_id).page_content)