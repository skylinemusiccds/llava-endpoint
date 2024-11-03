# text_to_speech.py

import os
from elevenlabs import VoiceSettings, ElevenLabs

ELEVENLABS_API_KEY = "sk_29eaa30255601541b3a80f470ac8c45987c007b8e2dfb791"
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_file(text: str) -> str:
    # Calling the text-to-speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="XrExE9yKIg1WjnnlVkGX",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = "output.wav"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path

