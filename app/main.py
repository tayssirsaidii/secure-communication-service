from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.encryption import encrypt_bytes, decrypt_bytes
from app.filters import is_content_authorized
import io

app = FastAPI()

@app.post("/encrypt")
async def encrypt_file(file: UploadFile = File(...)):
    file_content = await file.read()# نقرا محتوى الملف


    # Content control
    authorized, message = is_content_authorized(file.filename, file_content)
    if not authorized:
        raise HTTPException(status_code=400, detail=message)

    encrypted_data = encrypt_bytes(file_content)

    return StreamingResponse(
        io.BytesIO(encrypted_data),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file.filename}.enc"}
    )

@app.post("/decrypt")
async def decrypt_file(file: UploadFile = File(...)):
    encrypted_content = await file.read()

    try:
        decrypted_data = decrypt_bytes(encrypted_content)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or tampered encrypted file.")

    return StreamingResponse(
        io.BytesIO(decrypted_data),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename=decrypted_{file.filename.replace('.enc', '')}"}
    )
@app.get("/status")
async def service_status():
    return {"status": "Online"}
