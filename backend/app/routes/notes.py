from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import get_db
from app.models.orm_models import Note, User
from app.routes.auth import get_current_user
from app.services.ai_service import ai_service

router = APIRouter()


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    category: Optional[str] = "Personal"
    is_favorite: Optional[bool] = False
    favorite: Optional[bool] = False
    is_locked: Optional[bool] = False
    locked: Optional[bool] = False


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    is_favorite: Optional[bool] = None
    favorite: Optional[bool] = None
    is_locked: Optional[bool] = None
    locked: Optional[bool] = None


def format_note(note: Note):
    return {
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "category": note.category or "Personal",
        "tags": note.tags or [],
        "favorite": bool(note.is_favorite),
        "is_favorite": bool(note.is_favorite),
        "locked": bool(note.is_locked),
        "is_locked": bool(note.is_locked),
        "created_at": note.created_at.isoformat() if note.created_at else None,
        "updated_at": note.updated_at.isoformat() if note.updated_at else None
    }


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    fav = note.favorite if note.favorite is not None else note.is_favorite
    lock = note.locked if note.locked is not None else note.is_locked
    
    new_note = Note(
        user_id=current_user.id,
        title=note.title,
        content=note.content,
        category=note.category or "Personal",
        tags=note.tags or [],
        is_favorite=bool(fav),
        is_locked=bool(lock)
    )
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return format_note(new_note)


@router.get("")
@router.get("/")
async def get_notes(
    category: Optional[str] = None,
    favorite_only: Optional[bool] = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Note).filter(Note.user_id == current_user.id)
    
    if category and category.lower() != "all":
        query = query.filter(Note.category == category)
    if favorite_only:
        query = query.filter(Note.is_favorite == True)
    
    notes = query.order_by(Note.created_at.desc()).all()
    return [format_note(n) for n in notes]


@router.get("/{note_id}")
async def get_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return format_note(note)


@router.put("/{note_id}")
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    update_data = note_update.dict(exclude_unset=True)
    if "favorite" in update_data:
        update_data["is_favorite"] = update_data.pop("favorite")
    if "locked" in update_data:
        update_data["is_locked"] = update_data.pop("locked")
    
    for field, value in update_data.items():
        if hasattr(note, field):
            setattr(note, field, value)
    
    db.commit()
    db.refresh(note)
    return format_note(note)


@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}


@router.post("/{note_id}/summarize")
async def summarize_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    try:
        summary = await ai_service.summarize_note(note_content=note.content)
        return {"note_id": note_id, "summary": summary}
    except Exception as e:
        words = note.content.split()
        brief = " ".join(words[:25]) + ("..." if len(words) > 25 else "")
        return {"note_id": note_id, "summary": f"Summary: {brief}"}
