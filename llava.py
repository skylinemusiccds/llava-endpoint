# llava.py

from speech_to_text import transcribe_audio
from text_to_speech import text_to_speech_file
import google.generativeai as genai

# Configure the Generative AI model
genai.configure(api_key="AIzaSyCYtC5PJdZfJwHB9q0C7Ohs2RNjALiGbbA")  # Replace with your actual Google API key
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="you are LLAVA, a conversational assistant designed to chat naturally, just like a human. Respond in a friendly, conversational tone with short responses that feel live and engaging. Keep responses under 70 words, focusing on natural conversation flow. Avoid technical or code-like language, keeping it casual and interactive.",
)
def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

def main(audio_file: str):
    # Step 1: Transcribe audio to text
    transcript = transcribe_audio(audio_file)
    print("Transcript:", transcript)

    # Step 2: Generate response from the LLM
    if transcript:
        response_text = generate_response(transcript)
        print("LLM Response:", response_text)

        # Step 3: Convert the response text to speech
        audio_output = text_to_speech_file(response_text)
        print(f"Generated audio file: {audio_output}")

if __name__ == "__main__":
    # Replace with the path to your audio file
    main("output.wav")
