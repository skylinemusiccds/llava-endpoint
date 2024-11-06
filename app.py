from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from speech_to_text import transcribe_audio
from text_to_speech import text_to_speech_file
import google.generativeai as genai
import os
import logging

app = FastAPI()

# Configure the Generative AI model
genai.configure(api_key="AIzaSyCYtC5PJdZfJwHB9q0C7Ohs2RNjALiGbbA")
model = genai.GenerativeModel("gemini-1.5-flash")

# Temporary file location for storing the TTS response
TEMP_AUDIO_FILE = "response_audio.wav"

@app.get("/")
async def root():
    return {"message": "Endpoint API is running!"}

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    try:
        # Save the uploaded audio file
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # Transcribe audio to text
        transcript = transcribe_audio(file_location)
        
        # Generate response from LLM
        if transcript:
            response_text = generate_response(transcript)
            
            # Convert response text to speech and save
            audio_output = text_to_speech_file(response_text)
            os.rename(audio_output, TEMP_AUDIO_FILE)
            
            os.remove(file_location)  # Cleanup uploaded audio file
        else:
            raise HTTPException(status_code=400, detail="No transcript available.")

        return {"message": "Audio processed successfully"}
    
    except Exception as e:
        logging.error("Error processing audio: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/get-response-audio/")
async def get_response_audio():
    if os.path.exists(TEMP_AUDIO_FILE):
        return FileResponse(TEMP_AUDIO_FILE, media_type="audio/wav")
    else:
        raise HTTPException(status_code=404, detail="Audio file not found")

# Clean up audio file after playback request
@app.delete("/get-response-audio/")
async def delete_response_audio():
    try:
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)
        return {"message": "Audio file deleted"}
    except Exception as e:
        logging.error("Error deleting audio: %s", e)
        raise HTTPException(status_code=500, detail="Failed to delete audio file")
