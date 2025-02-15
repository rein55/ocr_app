# app/api.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.ocr import DonutOCR
from utils.logger import setup_logger
from io import BytesIO

app = FastAPI()
logger = setup_logger("FastAPI")

# Inisialisasi OCR processor
try:
    ocr_processor = DonutOCR()
except Exception as e:
    logger.error("Gagal inisialisasi DonutOCR: %s", str(e))
    raise e

@app.get("/")
async def root():
    return {"message": "Donut OCR API sudah berjalan."}

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    logger.info("Menerima file: %s", file.filename)
    try:
        contents = await file.read()
        image_file = BytesIO(contents)
        result = ocr_processor.process_image(image_file)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error("Error di endpoint OCR: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
