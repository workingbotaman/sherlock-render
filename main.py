import re
from faker import Faker
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from collections import defaultdict
from presidio_image_redactor import ImageRedactorEngine
from PIL import Image
from flask import Flask, request, jsonify
from io import BytesIO
from pyngrok import ngrok
from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import base64

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class image_input(BaseModel):
  image: UploadFile

class text_input(BaseModel):
  text: str

analyzer = AnalyzerEngine()
redactor = ImageRedactorEngine()

@app.post('/text')
async def analyze_text(input_text : text_input):
  analyzed_text = analyzer.analyze(input_text.text, language="en")
  for res in analyzed_text:
    print(res)

  return f"Running"

@app.post('/image')
async def redact_image(file: UploadFile=File(...)):
  try:
    return {"received_file": file.filename, "content_type": file.content_type}
    # if not input_data.image.content_type.startswith('image/'):
    #   raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # image_data = await input_data.image.read()
    # redacted_image = redactor.redact(image_data)

    # return {"message": "Image redacted successfully"}

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
