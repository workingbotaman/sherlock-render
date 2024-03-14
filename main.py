from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from collections import defaultdict
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class text_input(BaseModel):
  text: str

analyzer = AnalyzerEngine()

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
