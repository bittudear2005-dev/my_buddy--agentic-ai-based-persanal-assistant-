from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime

from app.database import get_db
from app.models.orm_models import Task, User
from app.routes.auth import get_current_user
from app.services.ai_service import ai_service

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[Union[int, str]] = 3
    deadline: Optional[str] = None
    due_date: Optional[datetime] = None
    scheduled_time: Optional[str] = None
    scheduledTime: Optional[str] = None
    duration: Optional[int] = 60
    estimated_hours: Optional[float] = None
    category: Optional[str] = "General"
    status: Optional[str] = "pending"
    completed: Optional[bool] = False
    tags: List[str] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Union[int, str]] = None
    deadline: Optional[str] = None
    due_date: Optional[datetime] = None
    scheduled_time: Optional[str] = None
    scheduledTime: Optional[str] = None
    duration: Optional[int] = None
    estimated_hours: Optional[float] = None
    category: Optional[str] = None
    status: Optional[str] = None
    completed: Optional[bool] = None
    tags: Optional[List[str]] = None


def normalize_priority(val: Optional[Union[int, str]]) -> int:
    if val is None:
        return 3
    if isinstance(val, int):
        return max(1, min(5, val))
    val_str = str(val).lower()
    if val_str in ("urgent", "high", "5", "4"):
        return 5 if val_str in ("urgent", "5") else 4
    if val_str in ("medium", "3"):
        return 3
    if val_str in ("low", "2", "1"):
        return 2 if val_str == "2" else 1
    try:
        return max(1, min(5, int(val_str)))
    except ValueError:
        return 3


def format_task(task: Task):
    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description or "",
        "priority": task.priority or 3,
        "deadline": task.deadline or "",
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "scheduledTime": task.scheduled_time or "",
        "scheduled_time": task.scheduled_time or "",
        "duration": task.duration or 60,
        "estimated_hours": task.estimated_hours,
        "status": task.status or "pending",
        "completed": bool(task.completed or task.status == "completed"),
        "category": task.category or "General",
        "tags": task.tags or [],
        "created_at": task.created_at.isoformat() if task.created_at else None
    }


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sched_time = task.scheduled_time or task.scheduledTime
    new_task = Task(
        user_id=current_user.id,
        title=task.title,
        description=task.description,
        priority=normalize_priority(task.priority),
        deadline=task.deadline,
        due_date=task.due_date,
        scheduled_time=sched_time,
        duration=task.duration or 60,
        estimated_hours=task.estimated_hours,
        category=task.category or "General",
        status=task.status or ("completed" if task.completed else "pending"),
        completed=bool(task.completed or task.status == "completed"),
        tags=task.tags or []
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return format_task(new_task)


@router.get("")
@router.get("/")
async def get_tasks(
    status_filter: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    if category:
        query = query.filter(Task.category == category)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return [format_task(t) for t in tasks]


@router.get("/{task_id}")
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return format_task(task)


@router.put("/{task_id}")
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    if "priority" in update_data and update_data["priority"] is not None:
        update_data["priority"] = normalize_priority(update_data["priority"])
    if "scheduledTime" in update_data and "scheduled_time" not in update_data:
        update_data["scheduled_time"] = update_data.pop("scheduledTime")
    if "completed" in update_data and update_data["completed"] is not None:
        if update_data["completed"]:
            update_data["status"] = "completed"
        elif task.status == "completed":
            update_data["status"] = "pending"
    
    for field, value in update_data.items():
        if hasattr(task, field):
            setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return format_task(task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/analyze")
async def analyze_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        analysis = await ai_service.analyze_task(
            task_title=task.title,
            task_description=task.description or ""
        )
        return {"task_id": task_id, "analysis": analysis}
    except Exception as e:
        return {
            "task_id": task_id,
            "analysis": f"Task: {task.title}. Priority: {task.priority}/5. Suggested subtasks: 1. Plan requirements 2. Execute implementation 3. Verify results."
        }
