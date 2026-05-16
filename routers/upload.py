from fastapi import APIRouter, UploadFile, File, HTTPException
from services.file_handler import save_upload, prepare_image
from services.ocr import extract_cbc_values
from services.predictor import predict_cbc

router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}


@router.post("/cbc")
async def upload_cbc(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"نوع الملف مش مدعوم")

    try:
        file_path  = save_upload(file)
        image_path = prepare_image(file_path)
        lab_values = extract_cbc_values(image_path)
        diagnosis, confidence = predict_cbc(lab_values)

        return {
            "diagnosis":  diagnosis,
            "confidence": confidence,
            "values":     lab_values,
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))