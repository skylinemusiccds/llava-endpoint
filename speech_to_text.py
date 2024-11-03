# speech_to_text.py

import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, FileSource

load_dotenv()

API_KEY = os.getenv("DEEPGRAM_API_KEY", "4e6f0424fbfb3b7d04b1696a422a973af7fc057a")
deepgram = DeepgramClient(API_KEY)

def transcribe_audio(file_path: str) -> str:
    try:
        with open(file_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        return transcript

    except Exception as e:
        print(f"Exception in transcribing audio: {e}")
        return ""
