import os
import asyncio
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone
)

load_dotenv()

API_KEY = os.getenv("DEEPGRAM_API_KEY")

class Merge_Transcript:

    def reset(self):
        self.transcript_parts = []

    def __init__(self):
        self.reset()

    def add_new_sentence(self, sentence):
        self.transcript_parts.append(sentence)

    def get_full_sentence(self):
        return ",".join(self.transcript_parts)
    
merge_transcript = Merge_Transcript()

async def get_transcript():

    try:
    
        df_config = DeepgramClientOptions(
            options={
                "keepalive": "true"
            }
        )

        deepgram = DeepgramClient(API_KEY, df_config)

        dg_conection = deepgram.listen.asynclive.v("1")

        async def message_on(self, result, **kwargs):
            
            sentence = result.channel.alternatives[0].transcript
            # print(sentence)

            if not result.speech_final:
                merge_transcript.add_new_sentence(sentence)
            else:
                merge_transcript.add_new_sentence(sentence)
                full_sentence = merge_transcript.get_full_sentence()
                print(f"Speaker: {full_sentence}")
                
                merge_transcript.reset()

        async def error_on(self, error, **kwargs):
            print(f"\n\n{error}\n\n")
    
        dg_conection.on(LiveTranscriptionEvents.Transcript, message_on)
        dg_conection.on(LiveTranscriptionEvents.Error, error_on)

        options = LiveOptions(
            model="nova-2",
            language="zh-TW",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            smart_format=True,
            endpointing=380
        )

        await dg_conection.start(options)

        microphone = Microphone(dg_conection.send)

        microphone.start()

        while True:
            if not microphone.is_active():
                break
            await asyncio.sleep(1)

        microphone.finish()

        dg_conection.finish()

        print("Finished")
    
    except Exception as error:
        print(f"Failed to connected: {error}")
        return


if __name__=="__main__":
    asyncio.run(get_transcript())