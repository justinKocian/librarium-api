from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil, os
from uuid import uuid4
from app.dependencies.auth import get_current_admin

UPLOAD_DIR = "uploads"

router = APIRouter()

@router.post("/cover")
def upload_cover(file: UploadFile = File(...), admin=Depends(get_current_admin)):
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"cover_path": path}
