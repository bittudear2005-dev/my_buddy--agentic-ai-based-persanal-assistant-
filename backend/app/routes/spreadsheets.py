from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

from app.database import get_db
from app.models.orm_models import Spreadsheet, User
from app.routes.auth import get_current_user
from app.services.ai_service import ai_service

router = APIRouter()


class SpreadsheetCreate(BaseModel):
    name: str
    template_type: Optional[str] = "custom"
    description: Optional[str] = None
    headers: List[str] = []
    data: List[List[Any]] = []


class SpreadsheetUpdate(BaseModel):
    name: Optional[str] = None
    template_type: Optional[str] = None
    description: Optional[str] = None
    headers: Optional[List[str]] = None
    data: Optional[List[List[Any]]] = None


def format_spreadsheet(s: Spreadsheet):
    return {
        "id": str(s.id),
        "name": s.name,
        "template": s.template_type or "custom",
        "template_type": s.template_type or "custom",
        "description": s.description or "",
        "headers": s.headers or [],
        "data": s.data or [],
        "rows_count": len(s.data) if s.data else 0,
        "createdAt": s.created_at.strftime("%Y-%m-%d") if s.created_at else datetime.now().strftime("%Y-%m-%d"),
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "updated_at": s.updated_at.isoformat() if s.updated_at else None
    }


@router.get("")
@router.get("/")
async def get_spreadsheets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sheets = db.query(Spreadsheet).filter(
        Spreadsheet.user_id == current_user.id
    ).order_by(Spreadsheet.created_at.desc()).all()
    return [format_spreadsheet(s) for s in sheets]


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_spreadsheet(
    sheet: SpreadsheetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_sheet = Spreadsheet(
        user_id=current_user.id,
        name=sheet.name,
        template_type=sheet.template_type or "custom",
        description=sheet.description,
        headers=sheet.headers,
        data=sheet.data,
        rows_count=len(sheet.data) if sheet.data else 0
    )
    db.add(new_sheet)
    db.commit()
    db.refresh(new_sheet)
    return format_spreadsheet(new_sheet)


@router.get("/{sheet_id}")
async def get_spreadsheet(
    sheet_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sheet = db.query(Spreadsheet).filter(
        Spreadsheet.id == sheet_id,
        Spreadsheet.user_id == current_user.id
    ).first()
    
    if not sheet:
        raise HTTPException(status_code=404, detail="Spreadsheet not found")
    
    return format_spreadsheet(sheet)


@router.put("/{sheet_id}")
async def update_spreadsheet(
    sheet_id: str,
    sheet_update: SpreadsheetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sheet = db.query(Spreadsheet).filter(
        Spreadsheet.id == sheet_id,
        Spreadsheet.user_id == current_user.id
    ).first()
    
    if not sheet:
        raise HTTPException(status_code=404, detail="Spreadsheet not found")
    
    update_data = sheet_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(sheet, field):
            setattr(sheet, field, value)
    
    if sheet.data:
        sheet.rows_count = len(sheet.data)
    
    db.commit()
    db.refresh(sheet)
    return format_spreadsheet(sheet)


@router.delete("/{sheet_id}")
async def delete_spreadsheet(
    sheet_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sheet = db.query(Spreadsheet).filter(
        Spreadsheet.id == sheet_id,
        Spreadsheet.user_id == current_user.id
    ).first()
    
    if not sheet:
        raise HTTPException(status_code=404, detail="Spreadsheet not found")
    
    db.delete(sheet)
    db.commit()
    return {"message": "Spreadsheet deleted successfully"}


@router.post("/{sheet_id}/analyze")
async def analyze_spreadsheet(
    sheet_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sheet = db.query(Spreadsheet).filter(
        Spreadsheet.id == sheet_id,
        Spreadsheet.user_id == current_user.id
    ).first()
    
    if not sheet:
        raise HTTPException(status_code=404, detail="Spreadsheet not found")
    
    summary_prompt = f"Spreadsheet '{sheet.name}' has columns: {sheet.headers}. Rows: {len(sheet.data or [])}."
    try:
        response = await ai_service.chat(
            message=f"Analyze this spreadsheet summary: {summary_prompt}. Provide 3 quick insights or trends.",
            system_prompt="You are a data analyst assistant."
        )
        return {"sheet_id": sheet_id, "analysis": response.get("response", "")}
    except Exception as e:
        return {
            "sheet_id": sheet_id,
            "analysis": f"Spreadsheet '{sheet.name}' contains {len(sheet.headers)} columns and {len(sheet.data or [])} rows ready for tracking."
        }
