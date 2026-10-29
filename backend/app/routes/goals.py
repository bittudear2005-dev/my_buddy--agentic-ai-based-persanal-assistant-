from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.orm_models import Goal, User
from app.routes.auth import get_current_user

router = APIRouter()


class GoalCreate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    description: Optional[str] = None
    type: str = "daily"  # daily, longterm
    time: Optional[str] = None
    date: Optional[str] = None
    target_date: Optional[str] = None
    progress: Optional[int] = 0
    completed: Optional[bool] = False
    category: Optional[str] = "General"
    priority: Optional[str] = "medium"
    tags: List[str] = []


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    time: Optional[str] = None
    date: Optional[str] = None
    target_date: Optional[str] = None
    progress: Optional[int] = None
    completed: Optional[bool] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None


def format_goal(goal: Goal):
    return {
        "id": str(goal.id),
        "title": goal.title or goal.text or "",
        "text": goal.text or goal.title or "",
        "description": goal.description or "",
        "type": goal.type or "daily",
        "time": goal.time or "",
        "date": goal.date or "",
        "targetDate": goal.target_date or "",
        "target_date": goal.target_date or "",
        "progress": goal.progress or 0,
        "completed": bool(goal.completed),
        "category": goal.category or "General",
        "priority": goal.priority or "medium",
        "status": goal.status or "active",
        "tags": goal.tags or [],
        "created_at": goal.created_at.isoformat() if goal.created_at else None
    }


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    title = goal.title or goal.text or "Untitled Goal"
    text = goal.text or goal.title or title
    
    new_goal = Goal(
        user_id=current_user.id,
        title=title,
        text=text,
        description=goal.description,
        type=goal.type,
        time=goal.time,
        date=goal.date,
        target_date=goal.target_date,
        progress=goal.progress or 0,
        completed=bool(goal.completed),
        category=goal.category or "General",
        priority=goal.priority or "medium",
        tags=goal.tags or []
    )
    
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    
    return format_goal(new_goal)


@router.get("")
@router.get("/")
async def get_goals(
    type: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Goal).filter(Goal.user_id == current_user.id)
    
    if type:
        query = query.filter(Goal.type == type)
    if status_filter:
        query = query.filter(Goal.status == status_filter)
    
    goals = query.order_by(Goal.created_at.desc()).all()
    return [format_goal(g) for g in goals]


@router.get("/{goal_id}")
async def get_goal(
    goal_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return format_goal(goal)


@router.put("/{goal_id}")
async def update_goal(
    goal_id: str,
    goal_update: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    update_data = goal_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(goal, field):
            setattr(goal, field, value)
    
    db.commit()
    db.refresh(goal)
    return format_goal(goal)


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}
