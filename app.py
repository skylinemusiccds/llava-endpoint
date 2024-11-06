from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import os
import logging
import asyncio
import google.generativeai as genai
from speech_to_text import transcribe_audio  # Ensure you have this module implemented
from text_to_speech import text_to_speech_file  # Ensure you have this module implemented

# Initialize FastAPI application
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# CORS Configuration for cross-origin requests
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Google Gemini (Generative AI) model
genai.configure(api_key="AIzaSyCYtC5PJdZfJwHB9q0C7Ohs2RNjALiGbbA")  # Replace with your actual Google API key
model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with your correct model

def generate_response(prompt: str) -> str:
    """
    Uses Google Gemini to generate a response from the input prompt.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error("Error generating response from LLM: %s", e)
        raise HTTPException(status_code=500, detail="Error generating response from LLM.")

@app.get("/")
async def root():
    return {"message": "Service is running!"}

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    """
    Handles audio file upload, transcribes it to text, generates a response,
    converts the response into speech, and streams the audio back to the client.
    """
    logging.info("Received file: %s", file.filename)

    file_location = f"temp_{file.filename}"
    try:
        # Step 1: Save the uploaded audio file
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        logging.info("Audio file saved to: %s", file_location)

        # Step 2: Transcribe audio to text
        transcript = transcribe_audio(file_location)
        logging.info("Transcript: %s", transcript)

        # Step 3: Generate response from the LLM
        response_text = ""
        if transcript:
            response_text = generate_response(transcript)
            logging.info("LLM Response: %s", response_text)

            # Step 4: Convert the response text to speech
            audio_output = text_to_speech_file(response_text)
            logging.info("Generated audio file: %s", audio_output)

            # Optional: Clean up temporary files
            os.remove(file_location)  # Remove the uploaded file after processing
        else:
            logging.warning("No transcript generated.")
            raise HTTPException(status_code=400, detail="No transcript available.")

        # Define a generator to stream the audio file in chunks
        async def audio_streamer(file_path: str):
            try:
                with open(file_path, "rb") as audio_file:
                    while chunk := audio_file.read(1024):  # Adjust chunk size if needed
                        yield chunk
                    await asyncio.sleep(1)  # Ensure the final chunk is sent
            finally:
                os.remove(file_path)  # Delete audio file after playback is done
                logging.info("Deleted audio file after streaming: %s", file_path)

        # Return the generated audio file as a streaming response
        return StreamingResponse(audio_streamer(audio_output), media_type='audio/wav')

    except Exception as e:
        logging.error("Error processing audio: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

