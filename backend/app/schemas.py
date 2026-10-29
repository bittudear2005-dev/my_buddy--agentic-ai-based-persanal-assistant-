"""
Pydantic Schemas for Request/Response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ============================================
# USER SCHEMAS
# ============================================

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user response (no password)"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ============================================
# GOAL SCHEMAS
# ============================================

class DailyGoalCreate(BaseModel):
    """Schema for creating daily goal"""
    text: str = Field(..., min_length=1, max_length=500)
    time: Optional[str] = None  # HH:MM format
    date: Optional[str] = None  # YYYY-MM-DD format

class DailyGoalUpdate(BaseModel):
    """Schema for updating daily goal"""
    text: Optional[str] = None
    completed: Optional[bool] = None
    time: Optional[str] = None
    date: Optional[str] = None

class DailyGoalResponse(BaseModel):
    """Schema for daily goal response"""
    id: int
    user_id: int
    text: str
    completed: bool
    time: Optional[str]
    date: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class LongTermGoalCreate(BaseModel):
    """Schema for creating long-term goal"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    target_date: Optional[str] = None

class LongTermGoalUpdate(BaseModel):
    """Schema for updating long-term goal"""
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[str] = None
    progress: Optional[int] = Field(None, ge=0, le=100)

class LongTermGoalResponse(BaseModel):
    """Schema for long-term goal response"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    target_date: Optional[str]
    progress: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================
# NOTE SCHEMAS
# ============================================

class NoteCreate(BaseModel):
    """Schema for creating note"""
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None
    category: str = "Personal"
    tags: List[str] = []
    is_locked: bool = False

class NoteUpdate(BaseModel):
    """Schema for updating note"""
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None
    is_locked: Optional[bool] = None

class NoteResponse(BaseModel):
    """Schema for note response"""
    id: int
    user_id: int
    title: str
    content: Optional[str]
    category: str
    tags: List[str]
    is_favorite: bool
    is_locked: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============================================
# TASK SCHEMAS
# ============================================

class TaskCreate(BaseModel):
    """Schema for creating task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: int = Field(3, ge=1, le=5)
    deadline: Optional[str] = None
    scheduled_time: Optional[str] = None
    duration: int = Field(60, ge=1)  # minutes

class TaskUpdate(BaseModel):
    """Schema for updating task"""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    deadline: Optional[str] = None
    scheduled_time: Optional[str] = None
    duration: Optional[int] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    """Schema for task response"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    priority: int
    deadline: Optional[str]
    scheduled_time: Optional[str]
    duration: int
    status: str
    auto_rescheduled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================
# FILE SCHEMAS
# ============================================

class FileResponse(BaseModel):
    """Schema for file response"""
    id: int
    user_id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    storage_path: str
    ai_category: Optional[str]
    ai_description: Optional[str]
    ai_summary: Optional[str]
    tags: List[str]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# ============================================
# SPREADSHEET SCHEMAS
# ============================================

class SpreadsheetCreate(BaseModel):
    """Schema for creating spreadsheet"""
    name: str = Field(..., min_length=1, max_length=200)
    template_type: str = "custom"
    headers: List[str] = []
    data: List[List[str]] = []

class SpreadsheetUpdate(BaseModel):
    """Schema for updating spreadsheet"""
    name: Optional[str] = None
    headers: Optional[List[str]] = None
    data: Optional[List[List[str]]] = None

class SpreadsheetResponse(BaseModel):
    """Schema for spreadsheet response"""
    id: int
    user_id: int
    name: str
    template_type: str
    headers: List[str]
    data: List[List[str]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============================================
# AI SCHEMAS
# ============================================

class ChatMessage(BaseModel):
    """Schema for chat message"""
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    """Schema for chat request"""
    messages: List[ChatMessage]
    temperature: float = 0.7

class ChatResponse(BaseModel):
    """Schema for chat response"""
    content: str
    model: str
    tokens_used: int = 0

class SummarizeRequest(BaseModel):
    """Schema for summarization request"""
    text: str = Field(..., min_length=1)
    max_length: int = Field(100, ge=10, le=500)

class CategorizeRequest(BaseModel):
    """Schema for categorization request"""
    text: str
    categories: List[str]

class SearchRequest(BaseModel):
    """Schema for semantic search"""
    query: str
    content_type: Optional[str] = None  # "note", "file", "task"
    top_k: int = Field(5, ge=1, le=20)