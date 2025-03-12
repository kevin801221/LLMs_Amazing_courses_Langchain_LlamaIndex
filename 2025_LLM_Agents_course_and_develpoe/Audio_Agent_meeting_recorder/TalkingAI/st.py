import streamlit as st

st.title("Hello World!~")
st.header("Changed")
st.subheader("subheader")
st.write("This is something.")
st.markdown("""
This is 'Markdown' text.""")
st.latex("""
a^2 + b^2 = c^2""")
st.json("""{
    "key": "value"
}""")
st.code("""
print("Hello!")""")

st.success("Success Alert")
st.error("Error")

name = st.text_input(
    "Name",
    "Ken"
)
password = st.text_input(
    "Password",
    type="password"
)
st.text_area(
    "Message",
    "Type something"
)
st.date_input("Date")
st.time_input("Appointment")
age1 = st.number_input(
    "Age",
    min_value=1,
    max_value=100,
    step=1
)
age2 = st.slider(
    "Age",
    1,
    100,
    10
)
st.checkbox("I agree")
st.radio(
    "Gender",
    ("Male", "Female"))

enable = st.toggle("Enable")
if enable:
    st.write("Toggle is enable.")
    color = st.color_picker("Pick a color", "#00FF09")

import pandas as pd

def load_data(data) -> pd.DataFrame:
    return pd.read_csv(data)

df = load_data("City Weather.csv")

st.dataframe(df)
st.table(df.head(2))
# st.json(df.to_json())

st.audio(
    "output-sdk.wav",
    format="audio/wav",
    start_time=0
)

if st.button("Click me"):
    st.toast("This is a toast message!")

import time

if st.button("Compute"):
    with st.spinner("Computing..."):
        time.sleep(2)
        st.write("Done!")

prompt = st.chat_input(
    "You ask me something."
)

def stream_data(data, delay: float=0.06):
    for char in data:
        yield char
        time.sleep(delay)

if prompt:
    with st.chat_message("User"):
        st.write("How are you?")

        with st.spinner("Thinking..."):
            time.sleep(2)
            response = "Some text from streamlit."
            st.write_stream(stream_data(response))

home_tab, about_tab = st.tabs(["Home", "About"])

with home_tab:
    st.subheader("Home")
    st.text("Home Tab Content")
    with st.expander("This is a dataframe"):
        st.dataframe(df)

with about_tab:
    st.subheader("About us")
    st.text("About Us Form")
    with st.popover("Table"):
        st.table(df.head(5))