import os
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from core.database import provide_session
from core.models import PostModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

router = APIRouter(
    prefix="/post",
    tags=["post"],
)


def generate_unique_filename(file_name: str) -> str:
    # 파일 확장자 분리
    file_name_without_ext, ext = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name_without_ext + ext
    while os.path.exists(os.path.join("static", new_file_name)):
        new_file_name = f"{file_name_without_ext}_{counter}{ext}"
        counter += 1

    return new_file_name  # 튜플이 아닌 문자열로 반환


@router.post("/save_image")
async def upload_posting(
    uploaded_by: str = Form(...),
    product_name: str = Form(...),
    price: int = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(provide_session)
) -> dict:
    directory = os.path.join("static")
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 파일 이름 생성
    unique_filename = generate_unique_filename(file.filename)
    
    file_path = os.path.join(directory, unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # URL 생성
    path = f"https://port-0-market-m5h20ajhfe0ec0f1.sel4.cloudtype.app/static/{unique_filename}"

    # 데이터베이스에 저장
    db_post = PostModel(
       image_path=path,
       uploaded_by=uploaded_by,
       product_name=product_name,
       price=price,
       description=description,
       category=category
    )
    
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return {"message": "Image saved successfully", "file_path": file_path}


@router.get("/get_post")
async def get_post(db: AsyncSession = Depends(provide_session)):
    result = await db.execute(select(PostModel))
    post_data = result.scalars().all()
    if not post_data:
        raise HTTPException(status_code=404, detail="No posts found")
    return post_data