from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from speech_to_text import transcribe_audio
from text_to_speech import text_to_speech_file
import google.generativeai as genai
import os

# Initialize FastAPI application
app = FastAPI()

# Configure the Generative AI model
genai.configure(api_key="AIzaSyCYtC5PJdZfJwHB9q0C7Ohs2RNjALiGbbA")  # Replace with your actual Google API key
model = genai.GenerativeModel("gemini-1.5-flash")
system_instruction="You are LLAVA, a conversational assistant designed to chat naturally, just like a human. Respond in a friendly, conversational tone with short responses that feel live and engaging. Keep responses under 70 words, focusing on natural conversation flow. Avoid technical or code-like language, keeping it casual and interactive."

def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

@app.get("/")
async def root():
    return {"message": "Service is running!"}

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    # Save the uploaded audio file
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Step 1: Transcribe audio to text
    transcript = transcribe_audio(file_location)
    print("Transcript:", transcript)

    # Step 2: Generate response from the LLM
    response_text = ""
    if transcript:
        response_text = generate_response(transcript)
        print("LLM Response:", response_text)

        # Step 3: Convert the response text to speech
        audio_output = text_to_speech_file(response_text)
        print(f"Generated audio file: {audio_output}")

    # Return the generated audio file as a response
    return FileResponse(audio_output, media_type='audio/wav', filename=os.path.basename(audio_output))

# You can add additional endpoints or functionality as needed
