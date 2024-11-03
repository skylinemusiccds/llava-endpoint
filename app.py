# app.py

from fastapi import FastAPI, File, UploadFile
from llava import main
import shutil

app = FastAPI()

@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    # Save uploaded file to a temporary location
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call the main function from llava.py to process the file
    response_audio = main(file_path)

    return {"response_audio": response_audio}
