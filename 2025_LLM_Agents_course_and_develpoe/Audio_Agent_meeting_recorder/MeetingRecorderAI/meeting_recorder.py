import os
import time
import streamlit as st
import shutil
import subprocess
import requests
import json
import datetime
import threading
import asyncio
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    PrerecordedOptions,
    LiveTranscriptionEvents,
    Microphone
)

# 加載環境變數
load_dotenv()
API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class MeetingTranscript:
    """管理會議記錄的類"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.transcript_parts = []
        self.full_transcript = []
        self.speakers = {}
        self.current_speaker = None
        self.meeting_summary = None
        self.action_items = []
        self.meeting_start_time = datetime.datetime.now()
        self.duration = 0
    
    def add_new_sentence(self, sentence, speaker=None, confidence=0):
        """添加新的句子到記錄中"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # 如果有指定說話者
        if speaker is not None:
            # 更新或添加說話者
            if speaker not in self.speakers:
                self.speakers[speaker] = {
                    "sentences": 0,
                    "total_words": 0,
                    "speaking_time": 0
                }
            
            # 更新說話者統計
            words = len(sentence.split())
            self.speakers[speaker]["sentences"] += 1
            self.speakers[speaker]["total_words"] += words
            
            # 估算說話時間 (假設平均每個單詞0.5秒)
            speaking_time = words * 0.5
            self.speakers[speaker]["speaking_time"] += speaking_time
            
            self.current_speaker = speaker
        else:
            # 如果沒有指定說話者，使用當前說話者
            speaker = self.current_speaker if self.current_speaker else "未知說話者"
        
        # 添加到記錄部分
        self.transcript_parts.append(sentence)
        
        # 添加到完整記錄
        self.full_transcript.append({
            "timestamp": timestamp,
            "speaker": speaker,
            "text": sentence,
            "confidence": confidence
        })
    
    def get_current_sentence(self):
        """獲取當前句子"""
        return " ".join(self.transcript_parts)
    
    def get_full_transcript(self):
        """獲取完整記錄"""
        return self.full_transcript
    
    def get_formatted_transcript(self):
        """獲取格式化的完整記錄"""
        formatted = []
        for entry in self.full_transcript:
            formatted.append(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}")
        return "\n".join(formatted)
    
    def get_meeting_duration(self):
        """獲取會議持續時間"""
        duration = datetime.datetime.now() - self.meeting_start_time
        minutes, seconds = divmod(duration.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_speaker_statistics(self):
        """獲取說話者統計信息"""
        return self.speakers
    
    def clear_current_sentence(self):
        """清除當前句子"""
        self.transcript_parts = []
    
    def update_duration(self, duration):
        """更新會議持續時間"""
        self.duration = duration

# 創建全局會議記錄對象
meeting_transcript = MeetingTranscript()

class TextToSpeech:
    """文字轉語音類"""
    
    model = "aura-asteria-zh"
    
    @staticmethod
    def is_installed(lib_name: str):
        lib = shutil.which(lib_name)
        return lib is not None
    
    def speak(self, text):
        """將文字轉換為語音"""
        if not self.is_installed("ffplay"):
            raise ValueError("未找到 ffplay。如果需要使用音頻流，請安裝它。")
        
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

# 創建全局TTS對象
tts = TextToSpeech()

class SpeakerDiarization:
    """說話者區分類"""
    
    def __init__(self):
        self.deepgram = DeepgramClient(API_KEY)
        self.speaker_profiles = {}
        self.current_speaker_id = 0
    
    def identify_speaker(self, audio_data, num_speakers=None):
        """識別說話者"""
        try:
            options = PrerecordedOptions(
                model="nova-2",
                language="zh-TW",
                smart_format=True,
                diarize=True,
                summarize=True,
                detect_topics=True,
                utterances=True
            )
            
            if num_speakers:
                options.diarize_version = "latest"
                options.diarize_num_speakers = num_speakers
            
            response = self.deepgram.listen.prerecorded.v("1").transcribe_file(
                {"buffer": audio_data}, 
                options
            )
            
            return response
            
        except Exception as e:
            print(f"說話者識別錯誤: {e}")
            return None
    
    def assign_speaker_id(self, speaker_tag):
        """分配說話者ID"""
        if speaker_tag not in self.speaker_profiles:
            self.current_speaker_id += 1
            self.speaker_profiles[speaker_tag] = f"說話者 {self.current_speaker_id}"
        
        return self.speaker_profiles[speaker_tag]

# 創建全局說話者區分對象
speaker_diarization = SpeakerDiarization()

class AIProcessor:
    """AI處理類"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=OPENAI_API_KEY,
            temperature=0.1
        )
    
    def generate_summary(self, transcript):
        """生成會議摘要"""
        system = SystemMessagePromptTemplate.from_template(
            """
            你是一個專業的會議記錄助手。
            請根據提供的會議記錄生成一個簡潔但全面的摘要。
            摘要應包括：
            1. 會議的主要主題
            2. 討論的關鍵點
            3. 達成的任何決定或結論
            
            請使用繁體中文回答。
            """
        )
        human = HumanMessagePromptTemplate.from_template("{text}")
        
        prompt = ChatPromptTemplate.from_messages([
            system,
            human
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        response = chain.invoke({"text": transcript})
        
        return response
    
    def extract_action_items(self, transcript):
        """提取行動項目"""
        schema = {
            "properties": {
                "action_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "需要執行的行動"
                            },
                            "assignee": {
                                "type": "string",
                                "description": "負責人，如果有指定的話"
                            },
                            "deadline": {
                                "type": "string",
                                "description": "截止日期，如果有指定的話"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            "required": ["action_items"]
        }
        
        system = SystemMessagePromptTemplate.from_template(
            """
            你是一個專業的會議記錄助手。
            請從提供的會議記錄中提取所有行動項目。
            行動項目通常是會議期間分配給特定人員的任務或責任。
            請注意任何提到的截止日期。
            
            請使用繁體中文回答。
            """
        )
        human = HumanMessagePromptTemplate.from_template("{text}")
        
        prompt = ChatPromptTemplate.from_messages([
            system,
            human
        ])
        
        chain = create_extraction_chain(schema, self.llm)
        
        response = chain.invoke(transcript)
        
        return response["action_items"]
    
    def identify_speakers(self, transcript):
        """識別說話者"""
        system = SystemMessagePromptTemplate.from_template(
            """
            你是一個專業的會議記錄助手。
            請分析提供的會議記錄，並嘗試識別不同的說話者。
            根據說話風格、提到的名字和上下文來區分說話者。
            
            請使用繁體中文回答。
            """
        )
        human = HumanMessagePromptTemplate.from_template("{text}")
        
        prompt = ChatPromptTemplate.from_messages([
            system,
            human
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        response = chain.invoke({"text": transcript})
        
        return response

# 創建全局AI處理對象
ai_processor = AIProcessor()

# 修改的音頻流處理函數 - 添加超時和事件同步
async def process_audio_stream(callback):
    """處理音頻流"""
    print("process_audio_stream 函數已被調用")
    
    # 設置超時，防止永久阻塞
    timeout_seconds = 10
    
    try:
        dg_config = DeepgramClientOptions(
            options={"keepalive": "true"}
        )
        
        deepgram = DeepgramClient(
            API_KEY,
            dg_config
        )
        
        dg_connection = deepgram.listen.asynclive.v("1")
        print("正在聆聽...")
        
        # 使用event來同步異步處理
        transcription_received = asyncio.Event()
        
        async def message_on(self, result, **kwargs):
            """處理收到的消息"""
            # 獲取轉錄文本
            sentence = result.channel.alternatives[0].transcript
            
            # 獲取說話者標籤（如果有）
            speaker_tag = None
            confidence = 0
            
            if hasattr(result.channel, 'metadata') and hasattr(result.channel.metadata, 'speaker'):
                speaker_tag = result.channel.metadata.speaker
                speaker_id = speaker_diarization.assign_speaker_id(speaker_tag)
            else:
                speaker_id = None
            
            if not result.speech_final:
                meeting_transcript.add_new_sentence(sentence, speaker_id, confidence)
            else:
                meeting_transcript.add_new_sentence(sentence, speaker_id, confidence)
                full_sentence = meeting_transcript.get_current_sentence()
                
                if len(full_sentence.strip()) > 0:
                    full_sentence = full_sentence.strip()
                    print(f"{speaker_id if speaker_id else '未知說話者'}: {full_sentence}")
                    
                    callback(full_sentence, speaker_id)
                    meeting_transcript.clear_current_sentence()
                    transcription_received.set()  # 標記已收到轉錄
        
        async def error_on(self, error, **kwargs):
            """處理錯誤"""
            print(f"\n\n{error}\n\n")
            transcription_received.set()  # 出現錯誤也要設置事件
        
        dg_connection.on(LiveTranscriptionEvents.Transcript, message_on)
        dg_connection.on(LiveTranscriptionEvents.Error, error_on)
        
        options = LiveOptions(
            model="nova-2",
            language="zh-TW",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            smart_format=True,
            diarize=True,
            endpointing=380,
            interim_results=True
        )
        
        await dg_connection.start(options)
        
        microphone = Microphone(dg_connection.send)
        microphone.start()
        
        # 等待轉錄結果，但設置超時
        try:
            await asyncio.wait_for(transcription_received.wait(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            print(f"超時: {timeout_seconds}秒內未收到轉錄")
        
        microphone.finish()
        await dg_connection.finish()
        
    except Exception as error:
        print(f"無法處理音頻: {error}")
        return

class MeetingRecorderManager:
    """會議記錄管理器類"""
    
    def __init__(self):
        self.transcription_response = ""
        self.current_speaker = None
        self.recording = False
        self.meeting_title = "未命名會議"
        self.meeting_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.participants = []
        self.estimated_speakers = 2
    
    def set_meeting_info(self, title, participants, estimated_speakers):
        """設置會議信息"""
        self.meeting_title = title
        self.participants = participants
        self.estimated_speakers = estimated_speakers
    
    def start_recording(self):
        """開始記錄"""
        self.recording = True
        meeting_transcript.reset()
        print("錄音已開始")
    
    def stop_recording(self):
        """停止記錄"""
        self.recording = False
        print("錄音已停止")
    
    def generate_meeting_summary(self):
        """生成會議摘要"""
        transcript = meeting_transcript.get_formatted_transcript()
        summary = ai_processor.generate_summary(transcript)
        meeting_transcript.meeting_summary = summary
        return summary
    
    def extract_action_items(self):
        """提取行動項目"""
        transcript = meeting_transcript.get_formatted_transcript()
        action_items = ai_processor.extract_action_items(transcript)
        meeting_transcript.action_items = action_items
        return action_items
    
    def export_meeting_record(self, format="markdown"):
        """匯出會議記錄"""
        transcript = meeting_transcript.get_formatted_transcript()
        summary = meeting_transcript.meeting_summary or "未生成摘要"
        action_items = meeting_transcript.action_items or []
        duration = meeting_transcript.get_meeting_duration()
        speakers = meeting_transcript.get_speaker_statistics()
        
        if format == "markdown":
            # 生成Markdown格式的會議記錄
            md_content = f"# {self.meeting_title}\n\n"
            md_content += f"日期: {self.meeting_date}\n"
            md_content += f"持續時間: {duration}\n"
            md_content += f"參與者: {', '.join(self.participants)}\n\n"
            
            md_content += "## 摘要\n\n"
            md_content += f"{summary}\n\n"
            
            md_content += "## 行動項目\n\n"
            for item in action_items:
                assignee = f" (@{item.get('assignee', '未分配')})" if item.get('assignee') else ""
                deadline = f" - 截止日期: {item.get('deadline')}" if item.get('deadline') else ""
                md_content += f"- {item.get('action')}{assignee}{deadline}\n"
            
            md_content += "\n## 說話者統計\n\n"
            for speaker, stats in speakers.items():
                md_content += f"### {speaker}\n"
                md_content += f"- 發言次數: {stats['sentences']}\n"
                md_content += f"- 總字數: {stats['total_words']}\n"
                md_content += f"- 發言時間: {stats['speaking_time']:.1f} 秒\n\n"
            
            md_content += "## 完整記錄\n\n"
            md_content += "```\n"
            md_content += transcript
            md_content += "\n```\n"
            
            return md_content
        
        elif format == "json":
            # 生成JSON格式的會議記錄
            json_content = {
                "meeting_title": self.meeting_title,
                "meeting_date": self.meeting_date,
                "duration": duration,
                "participants": self.participants,
                "summary": summary,
                "action_items": action_items,
                "speaker_statistics": speakers,
                "transcript": meeting_transcript.get_full_transcript()
            }
            
            return json.dumps(json_content, ensure_ascii=False, indent=2)
        
        else:
            return "不支持的格式"
    
    # 改進的異步處理方法 - 避免無限循環阻塞
    async def start(self):
        """開始會議記錄"""
        print("MeetingRecorderManager 的 start 方法已被調用")
        
        def handle_full_sentence(full_sentence, speaker_id):
            """處理完整句子"""
            self.transcription_response = full_sentence
            self.current_speaker = speaker_id
            
            # 將數據存入session_state以便在下次UI刷新時顯示
            if 'transcript_history' not in st.session_state:
                st.session_state.transcript_history = []
            
            st.session_state.transcript_history.append({
                'speaker': speaker_id if speaker_id else "未知說話者",
                'text': full_sentence
            })
        
        # 使用有限次數嘗試而非無限循環
        max_attempts = 100  # 設置一個合理的嘗試次數上限
        attempts = 0
        
        # 當設置為錄音狀態且尚未達到嘗試上限時繼續執行
        while self.recording and attempts < max_attempts:
            attempts += 1
            try:
                await process_audio_stream(handle_full_sentence)
                
                # 如果已不再錄音則退出循環
                if not self.recording:
                    break
                    
                # 短暫暫停以允許其他處理
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"處理音頻時發生錯誤: {e}")
                # 短暫等待後重試
                await asyncio.sleep(1)
        
        print(f"錄音處理結束，進行了 {attempts} 次嘗試")

# 創建全局會議記錄管理器對象
manager = MeetingRecorderManager()

# 輔助函數，用於開始錄音並避免UI阻塞
def start_recording_and_rerun():
    """開始錄音並重新運行UI"""
    manager.start_recording()
    st.session_state.recording = True
    
    # 使用線程而非直接阻塞UI
    def start_recording_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(manager.start())
    
    st.session_state.recording_thread = threading.Thread(
        target=start_recording_thread,
        daemon=True
    )
    st.session_state.recording_thread.start()
    st.rerun()

def main():
    """主函數"""
    st.set_page_config(
        page_title="智能會議記錄助手",
        page_icon="📝",
        layout="wide"
    )
    
    # 初始化session_state
    if "recording" not in st.session_state:
        st.session_state.recording = False
    
    if "report_generated" not in st.session_state:
        st.session_state.report_generated = False
    
    if "recording_thread" not in st.session_state:
        st.session_state.recording_thread = None
    
    if "transcript_history" not in st.session_state:
        st.session_state.transcript_history = []
    
    if "duration_thread" not in st.session_state:
        st.session_state.duration_thread = None
    
    st.title("📝 智能會議記錄助手")
    st.subheader("自動記錄會議內容，識別說話者，並生成摘要和行動項目")
    
    # 側邊欄設置
    with st.sidebar:
        st.header("會議設置")
        
        meeting_title = st.text_input(
            "會議標題",
            placeholder="輸入會議標題",
            key="meeting_title"
        )
        
        meeting_participants = st.text_input(
            "參與者 (用逗號分隔)",
            placeholder="例如: 張三, 李四, 王五",
            key="meeting_participants"
        )
        
        estimated_speakers = st.number_input(
            "預估說話者數量",
            min_value=1,
            max_value=10,
            value=2,
            key="estimated_speakers"
        )
        
        if meeting_title and meeting_participants:
            participants = [p.strip() for p in meeting_participants.split(",") if p.strip()]
            manager.set_meeting_info(meeting_title, participants, estimated_speakers)
        
        st.divider()
        
        # 控制按鈕
        st.subheader("控制面板")
        col1, col2 = st.columns(2)
        
        with col1:
            if not st.session_state.recording:
                if st.button("🎙️ 開始記錄", use_container_width=True, key="sidebar_start_button"):
                    start_recording_and_rerun()
            else:
                if st.button("⏹️ 停止記錄", use_container_width=True, key="sidebar_stop_button"):
                    manager.stop_recording()
                    st.session_state.recording = False
                    st.rerun()
        
        with col2:
            # 只有在非錄製狀態且有記錄數據時顯示此按鈕
            if not st.session_state.recording and meeting_transcript.get_full_transcript():
                if st.button("📊 生成報告", use_container_width=True, key="sidebar_report_button"):
                    with st.spinner("正在生成會議報告..."):
                        summary = manager.generate_meeting_summary()
                        action_items = manager.extract_action_items()
                        st.session_state.report_generated = True
                        st.rerun()
    
    # 主界面控制按鈕（增加可見性）
    if not st.session_state.recording and not st.session_state.report_generated:
        main_start_button = st.button(
            "🎙️ 開始記錄 (主界面)", 
            key="main_start_button",
            use_container_width=True
        )
        
        if main_start_button:
            start_recording_and_rerun()
            
    elif st.session_state.recording:
        # 顯示停止按鈕和錄音狀態
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("⏹️ 停止錄音", key="main_stop_button", use_container_width=True):
                manager.stop_recording()
                st.session_state.recording = False
                st.rerun()
        with col2:
            st.info("🎙️ 正在記錄會議... 請說話", icon="🔴")
    
    # 主要內容區域
    if st.session_state.recording:
        # 顯示會議時間
        duration_placeholder = st.empty()
        
        # 顯示實時記錄
        transcript_container = st.container()
        with transcript_container:
            st.subheader("實時記錄")
            st.markdown("---")
            
            # 顯示已有的記錄歷史
            for entry in st.session_state.transcript_history:
                st.markdown(f"**{entry['speaker']}**: {entry['text']}")
        
        # 更新會議時間的函數
        def update_duration(meeting_transcript, duration_placeholder):
            """更新會議持續時間"""
            start_time = time.time()
            while st.session_state.recording:  # 使用session_state而非manager
                duration = time.time() - start_time
                meeting_transcript.update_duration(duration)
                minutes, seconds = divmod(duration, 60)
                hours, minutes = divmod(minutes, 60)
                duration_placeholder.write(f"會議持續時間: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
                time.sleep(1)
        
        # 在後台執行更新會議時間
        if st.session_state.duration_thread is None or not st.session_state.duration_thread.is_alive():
            st.session_state.duration_thread = threading.Thread(
                target=update_duration, 
                args=(meeting_transcript, duration_placeholder), 
                daemon=True
            )
            st.session_state.duration_thread.start()
    
    elif st.session_state.report_generated:
        # 添加匯出按鈕
        st.sidebar.divider()
        st.sidebar.subheader("匯出選項")
        export_format = st.sidebar.selectbox("選擇匯出格式", ["Markdown", "JSON"], key="export_format")
        
        if st.sidebar.button("匯出會議記錄", key="export_button"):
            format_lower = export_format.lower()
            exported_content = manager.export_meeting_record(format=format_lower)
            
            file_extension = "md" if format_lower == "markdown" else "json"
            filename = f"{manager.meeting_title.replace(' ', '_')}_{manager.meeting_date}.{file_extension}"
            
            st.sidebar.download_button(
                label=f"下載 {export_format} 文件",
                data=exported_content,
                file_name=filename,
                mime="text/plain" if format_lower == "markdown" else "application/json",
                key="download_button"
            )
        # 顯示會議報告
        st.success("✅ 會議記錄已完成")
        
        # 添加按鈕回到初始狀態
        if st.button("🔄 開始新會議", key="new_meeting_button"):
            st.session_state.report_generated = False
            st.session_state.transcript_history = []
            st.rerun()
        
        tab1, tab2, tab3, tab4 = st.tabs(["📝 摘要", "✅ 行動項目", "👥 說話者統計", "📜 完整記錄"])
        
        with tab1:
            st.subheader("會議摘要")
            st.markdown(meeting_transcript.meeting_summary)
        
        with tab2:
            st.subheader("行動項目")
            for item in meeting_transcript.action_items:
                assignee = f" (@{item.get('assignee', '未分配')})" if item.get('assignee') else ""
                deadline = f" - 截止日期: {item.get('deadline')}" if item.get('deadline') else ""
                st.markdown(f"- {item.get('action')}{assignee}{deadline}")
        
        with tab3:
            st.subheader("說話者統計")
            speakers = meeting_transcript.get_speaker_statistics()
            
            # 準備圖表數據
            speaker_names = list(speakers.keys())
            speaking_times = [stats["speaking_time"] for stats in speakers.values()]
            word_counts = [stats["total_words"] for stats in speakers.values()]
            
            # 顯示說話時間圖表
            if speaker_names:
                st.subheader("說話時間分佈")
                st.bar_chart(pd.DataFrame(
                    {"時間 (秒)": speaking_times},
                    index=speaker_names
                ))
                
                st.subheader("字數分佈")
                st.bar_chart(pd.DataFrame(
                    {"字數": word_counts},
                    index=speaker_names
                ))
                

            
            # 顯示詳細統計
            for speaker, stats in speakers.items():
                with st.expander(f"{speaker} 的詳細統計"):
                    st.markdown(f"- 發言次數: {stats['sentences']}")
                    st.markdown(f"- 總字數: {stats['total_words']}")
                    st.markdown(f"- 發言時間: {stats['speaking_time']:.1f} 秒")