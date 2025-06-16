from fastapi import APIRouter, UploadFile, File
import cloudinary.uploader
import os
from ..utils.pdf_extracter import extract_text_from_pdf
from ..config import cloudinary_config
from ..config.mongodb import uploads_collection
from ..utils.summarizer import summarize_text  # import the function
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Step 1: Save file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Step 2: Upload to Cloudinary
    try:
        result = cloudinary.uploader.upload(temp_path, resource_type="raw")
        cloud_url = result["secure_url"]
    except Exception as e:
        os.remove(temp_path)
        return {"error": f"Cloudinary upload failed: {str(e)}"}

    # Step 3: Extract text
    try:
        extracted_text = extract_text_from_pdf(temp_path)
    except Exception as e:
        os.remove(temp_path)
        return {"error": f"Text extraction failed: {str(e)}"}

    # Step 4: Delete the local file
    os.remove(temp_path)

    # Step 5: Save metadata in MongoDB
    upload_doc = {
        "filename": file.filename,
        "cloud_url": cloud_url,
        "text_preview": extracted_text[:300],
        "uploaded_at": datetime.utcnow()
    }
    try:
        await uploads_collection.insert_one(upload_doc)
        summary = await summarize_text(extracted_text)
        #print("Summary:", summary)

    except Exception as e:
        return {"error": f"MongoDB save failed: {str(e)}"}

    # Step 6: Return response
    return {
        "filename": file.filename,
        "cloud_url": cloud_url,
        "text": extracted_text,
        "summary": summary
    }
