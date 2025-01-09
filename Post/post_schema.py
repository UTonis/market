from core.database import Optional
from pydantic import BaseModel
from fastapi import UploadFile, File
class PostDTO(BaseModel):
    uploaded_by: str
    product_name: str
    price: int
    description: Optional[str] = None  # 선택적 필드로 처리
    category: Optional[str] = None  # 선택적 필드로 처리
    file: UploadFile = File(...)