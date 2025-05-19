from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import csv
import io
from datetime import datetime

from database import get_db, get_user_data_dir
from models import User, UserFile
from schemas import UserFileInfo
from auth import get_current_user

router = APIRouter(tags=["файлы"])

@router.post("/users/me/files/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Только CSV файлы разрешены")
    
    user_dir = get_user_data_dir(current_user.id)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(user_dir, f"{timestamp}_{file.filename}")
    
    content = await file.read()
    
    try:
        text_content = content.decode('utf-8')
        csv.reader(io.StringIO(text_content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Невалидный CSV файл: {str(e)}")
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    db_file = UserFile(
        filename=file.filename,
        upload_date=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        user_id=current_user.id
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return {"filename": file.filename, "status": "success"}

@router.get("/users/me/files/", response_model=List[UserFileInfo])
async def get_user_files(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    files = db.query(UserFile).filter(UserFile.user_id == current_user.id).all()
    return files


@router.get("/users/me/files/{file_id}/data/")
async def get_file_data(
    file_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = db.query(UserFile).filter(UserFile.id == file_id, UserFile.user_id == current_user.id).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    try:
        user_dir = get_user_data_dir(current_user.id)
        files = [f for f in os.listdir(user_dir) if f.endswith(file.filename)]
        
        if not files:
            raise HTTPException(status_code=404, detail="Файл не найден на диске")
        
        files.sort(reverse=True)
        file_path = os.path.join(user_dir, files[0])
        
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            data = []
            for row in csv_reader:
                string_row = {key: str(value) for key, value in row.items()}
                data.append(string_row)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения файла: {str(e)}")
    
@router.get("/users/{user_id}/files/", response_model=List[UserFileInfo])
async def get_user_files_by_id(
    user_id: int, 
    db: Session = Depends(get_db)
):
    files = db.query(UserFile).filter(UserFile.user_id == user_id).all()
    return files