import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


def generate_uuid():
    return str(uuid.uuid4())


# ============================================
# USER MODEL
# ============================================
class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    preferences = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    files = relationship("FileModel", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    spreadsheets = relationship("Spreadsheet", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("AIConversation", back_populates="user", cascade="all, delete-orphan")


# ============================================
# TASK MODEL
# ============================================
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, cancelled
    priority = Column(Integer, default=3)  # 1-5
    category = Column(String(100), default="General")
    deadline = Column(String(50), nullable=True)  # YYYY-MM-DD format
    due_date = Column(DateTime(timezone=True), nullable=True)
    scheduled_time = Column(String(50), nullable=True)  # HH:MM format
    duration = Column(Integer, default=60)  # duration in minutes
    estimated_hours = Column(Float, nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    auto_rescheduled = Column(Boolean, default=False)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="tasks")


# ============================================
# GOAL MODEL
# ============================================
class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    text = Column(String(500), nullable=True)  # Daily goal text
    description = Column(Text, nullable=True)
    type = Column(String(50), default="daily")  # daily, longterm
    time = Column(String(50), nullable=True)  # HH:MM format
    date = Column(String(50), nullable=True)  # YYYY-MM-DD format
    target_date = Column(String(50), nullable=True)
    progress = Column(Integer, default=0)  # 0-100 percentage
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    category = Column(String(100), default="General")
    priority = Column(String(50), default="medium")
    status = Column(String(50), default="active")  # active, completed, archived
    tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="goals")


# ============================================
# NOTE MODEL
# ============================================
class Note(Base):
    __tablename__ = "notes"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), default="Personal")  # Personal, Work, Ideas
    tags = Column(JSON, default=list)
    is_favorite = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    is_encrypted = Column(Boolean, default=False)
    encryption_key = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="notes")


# ============================================
# FILE MODEL
# ============================================
class FileModel(Base):
    __tablename__ = "files"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, image, video, audio, doc, etc.
    file_size = Column(Integer, nullable=False)  # bytes
    category = Column(String(100), default="Uncategorized")
    mime_type = Column(String(100), nullable=True)
    is_encrypted = Column(Boolean, default=False)
    file_metadata = Column(JSON, default=dict)
    ai_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="files")


# ============================================
# SPREADSHEET MODEL
# ============================================
class Spreadsheet(Base):
    __tablename__ = "spreadsheets"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    template_type = Column(String(100), default="custom")
    description = Column(Text, nullable=True)
    headers = Column(JSON, default=list)
    data = Column(JSON, default=list)
    columns = Column(JSON, default=list)
    rows_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="spreadsheets")


# ============================================
# AI MESSAGE MODEL
# ============================================
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    conversation_id = Column(String(100), index=True, nullable=False)
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    model = Column(String(100), nullable=True)  # groq, gemini, openai
    tokens_used = Column(Integer, default=0)
    message_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="messages")


# ============================================
# AI CONVERSATION MODEL
# ============================================
class AIConversation(Base):
    __tablename__ = "ai_conversations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    conversation_id = Column(String(100), index=True, nullable=True, default=generate_uuid)
    title = Column(String(255), default="New Conversation")
    user_message = Column(Text, nullable=True)
    ai_response = Column(Text, nullable=True)
    model = Column(String(100), nullable=True)
    total_messages = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="conversations")