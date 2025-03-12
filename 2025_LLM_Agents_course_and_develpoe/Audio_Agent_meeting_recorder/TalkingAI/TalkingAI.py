import os
import time
import streamlit as st
import shutil
import subprocess
import requests
from dotenv import load_dotenv
import asyncio
from langchain_groq import ChatGroq
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
    Microphone
)

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
API_KEY = os.getenv("DEEPGRAM_API_KEY")

class ModelProcessor:
    def __init__(self):
        
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.1
        )

        system = SystemMessagePromptTemplate.from_template(
                    """
                        Your name is Emma.
                        That is very important.
                        Your response must be under 20 words.
                    """
                )
        human = HumanMessagePromptTemplate.from_template("{text}")
        
        self.prompt = ChatPromptTemplate.from_messages([
               system,
               human
            ])
        
        self.conversation = self.prompt | self.llm

    def process(self, text):
        
        response = self.conversation.invoke({"text": text})

        return response

class Merge_Transcript:

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.transcipt_parts = []

    def add_new_sentence(self, sentence):
        self.transcipt_parts.append(sentence)

    def get_full_sentence(self):
        return " ".join(self.transcipt_parts)
    
merge_transcript = Merge_Transcript()

class TextToSpeech:
    model = "aura-asteria-en"

    @staticmethod
    def is_installed(lib_name: str):
        lib = shutil.which(lib_name)
        return lib is not None

    def speak(self, text):
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found. if you need to use stream audio, please install it.")
        
        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.model}"

        headers = {
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {"text": text}

        player_command = ["ffplay", "-autoexit", "-", '-nodisp']
        player_process = subprocess.Popen(
            player_command,
            stdin = subprocess.PIPE,
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL
        )

        with requests.post(DEEPGRAM_URL, headers=headers, json=payload, stream=True) as request:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    player_process.stdin.write(chunk)
                    player_process.stdin.flush()

        if player_process.stdin:
            player_process.stdin.close()
        player_process.wait()

tts = TextToSpeech()

async def get_transcript(callback):
    
    transcription_complete = asyncio.Event()

    try:
        dg_config = DeepgramClientOptions(
            options={"keepalive": "true"}
        )

        deepgram = DeepgramClient(
            API_KEY,
            dg_config
        )

        dg_connection = deepgram.listen.asynclive.v("1")
        print("Listening...")

        async def message_on(self, result, **kwargs):
            
            sentence = result.channel.alternatives[0].transcript

            if not result.speech_final:
                merge_transcript.add_new_sentence(sentence)
            else:
                merge_transcript.add_new_sentence(sentence)
                full_sentence = merge_transcript.get_full_sentence()

                if len(full_sentence.strip()) > 0:
                    full_sentence = full_sentence.strip()
                    print(f"Human: {full_sentence}")

                    callback(full_sentence)
                    merge_transcript.reset()
                    transcription_complete.set()

        async def error_on(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, message_on)
        dg_connection.on(LiveTranscriptionEvents.Error, error_on)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            smart_format=True,
            endpointing=380
        )

        await dg_connection.start(options)

        microphone = Microphone(dg_connection.send)
        microphone.start()

        # while True: 
        #     if not microphone.is_active():
        #         break
        #     await asyncio.sleep(5)
        await transcription_complete.wait()
        
        microphone.finish()
        await dg_connection.finish()

        print("Finished.")

        
    except Exception as error:
        print(f"Could not open web socket: {error}")
        return

class GetWebData:

    def __init__(self):
        self.embeddings_model = None
        self.vectorDB = None
        self.llm = ChatGroq(
            temperature=0.8,
            model="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def get_url_vectordb(self, url):

        loader = WebBaseLoader(url)
        document = loader.load()
        # st.write(document)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ""]
        )

        docs = text_splitter.split_documents(document)
        # st.write(docs)
        self.embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        self.vectorDB = FAISS.from_documents(docs, self.embeddings_model)
        self.vectorDB.save_local("faiss_db")

        return self.vectorDB

    def retrieval_generator(self, query, vectorDB):
        
        retriever = vectorDB.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        prompt = hub.pull("rlm/rag-prompt")

        rag_chain = (
            {
                "context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
                "question": RunnablePassthrough()
            }
            | prompt 
            | self.llm 
            | StrOutputParser()
        )

        response = rag_chain.invoke(query)
        
        return response

class AiManager:
    def __init__(self):
        self.transcription_response = ""
        self.llm = ModelProcessor()
        self.getwebdata = GetWebData()

    async def start(self, vectorDB):
        
        def stream_data(setence, delay: float = 0.05):
            for char in setence:
                yield char
                time.sleep(delay)

        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence
        
        query_box = st.empty()
        answer_box = st.empty()

        while True:
            await get_transcript(handle_full_sentence)

            if "goodbye" in self.transcription_response.lower():
                with query_box.container():
                    st.write_stream(
                        stream_data(self.transcription_response)
                    )
                
                llm_response = self.llm.process(self.transcription_response)

                with answer_box.container():
                    st.write_stream(
                        stream_data(llm_response.content)
                    )
                tts.speak(llm_response.content)
                
                break
            
            with query_box.container():
                st.write_stream(
                    stream_data(self.transcription_response)
                )
            
            # llm_response = self.llm.process(self.transcription_response)
            llm_response = self.getwebdata.retrieval_generator(self.transcription_response, vectorDB)

            with answer_box.container():
                st.write_stream(
                    stream_data(llm_response)
                )
            
            tts.speak(llm_response)

            self.transcription_response = ""


if __name__ == "__main__":
    manager = AiManager()
    getWebData = GetWebData()

    st.title("聊天💬機器人🤖")
    st.subheader("你可以向我提問，我會盡量回答您!")

    with st.sidebar:
        st.header("設定:")

        website_url = st.text_input(
            label="網址",
            placeholder="請輸入想要搜索🔍的網址"
        )

    if website_url is None or website_url =="":
        st.info("請輸入您想語音AI回答問題的網址.")
    else:
        st.info(f"現在語音AI已經可以根據{website_url}回答您的提問🙋")
        vectorDB = getWebData.get_url_vectordb(website_url)
        # getWebData.retrieval_generator("What is langchain?")
        asyncio.run(manager.start(vectorDB))