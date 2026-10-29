# 🧪 API Testing Guide

Complete guide to testing all API endpoints with curl and Python examples.

## 🔑 Authentication Flow

### 1. Register New User

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

**Response**:
```json
{
  "message": "User created successfully",
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "test@example.com",
    "full_name": "Test User"
  }
}
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Save Your Token

```bash
# Linux/Mac
export TOKEN="your_access_token_here"

# Windows (PowerShell)
$env:TOKEN="your_access_token_here"
```

---

## 🎯 Goals API

### Create Goal

```bash
curl -X POST http://localhost:8000/api/goals \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Launch my SaaS product",
    "description": "Build and launch a productivity SaaS",
    "target_date": "2025-06-01T00:00:00Z",
    "category": "business",
    "priority": "high",
    "tags": ["saas", "startup", "product"]
  }'
```

### List All Goals

```bash
curl -X GET http://localhost:8000/api/goals \
  -H "Authorization: Bearer $TOKEN"
```

### Update Goal

```bash
curl -X PUT http://localhost:8000/api/goals/{goal_id} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "progress": 25,
    "status": "active"
  }'
```

---

## ✅ Tasks API

### Create Task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design landing page",
    "description": "Create mockups for homepage",
    "due_date": "2025-02-01T00:00:00Z",
    "priority": "high",
    "category": "design",
    "estimated_hours": 8,
    "tags": ["design", "ui", "homepage"]
  }'
```

### List Tasks (with filters)

```bash
# All tasks
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"

# Only incomplete tasks
curl -X GET "http://localhost:8000/api/tasks?completed=false" \
  -H "Authorization: Bearer $TOKEN"

# High priority tasks
curl -X GET "http://localhost:8000/api/tasks?priority=high" \
  -H "Authorization: Bearer $TOKEN"
```

### Toggle Task Completion

```bash
curl -X POST http://localhost:8000/api/tasks/{task_id}/toggle \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📝 Notes API

### Create Note

```bash
curl -X POST http://localhost:8000/api/notes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Meeting Notes - Q1 Planning",
    "content": "Discussed roadmap for Q1. Key decisions: Launch 2 features...",
    "tags": ["meeting", "planning", "q1"],
    "category": "meetings",
    "is_favorite": false
  }'
```

### Search Notes

```bash
curl -X GET "http://localhost:8000/api/notes?search=planning&category=meetings" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📁 Files API

### Upload Single File

```bash
curl -X POST http://localhost:8000/api/files/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/document.pdf"
```

### Upload Multiple Files

```bash
curl -X POST http://localhost:8000/api/files/bulk-upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@document1.pdf" \
  -F "files=@image1.png" \
  -F "files=@spreadsheet.xlsx"
```

### List Files

```bash
curl -X GET http://localhost:8000/api/files \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🤖 AI Features

### 1. General Chat

```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Give me 5 productivity tips for software developers",
    "model": "gemini",
    "temperature": 0.7
  }'
```

### 2. Analyze Task

```bash
curl -X POST http://localhost:8000/api/ai/analyze-task \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_title": "Build authentication system",
    "task_description": "Implement JWT-based auth with social login"
  }'
```

**Response Example**:
```json
{
  "analysis": {
    "priority": "high",
    "estimated_hours": 40,
    "subtasks": [
      "Set up JWT library",
      "Create user model",
      "Implement registration",
      "Implement login",
      "Add social OAuth",
      "Set up password reset"
    ],
    "tips": [
      "Use bcrypt for password hashing",
      "Implement refresh tokens",
      "Add rate limiting"
    ]
  }
}
```

### 3. Summarize Note

```bash
curl -X POST http://localhost:8000/api/ai/summarize-note \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "note_content": "Long meeting notes here...",
    "summary_length": "medium"
  }'
```

### 4. Generate Goal Plan

```bash
curl -X POST http://localhost:8000/api/ai/generate-goal-plan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal_title": "Learn React and build 3 projects",
    "goal_description": "Want to become proficient in React",
    "target_date": "2025-06-01T00:00:00Z",
    "current_skills": ["JavaScript", "HTML", "CSS"]
  }'
```

### 5. Smart Suggestions

```bash
curl -X POST http://localhost:8000/api/ai/smart-suggestions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "I'\''m a software developer interested in machine learning",
    "suggestion_type": "goals"
  }'
```

### 6. Brainstorm Ideas

```bash
curl -X POST http://localhost:8000/api/ai/brainstorm \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "SaaS product ideas for developers",
    "num_ideas": 10
  }'
```

### 7. Rewrite Text

```bash
curl -X POST http://localhost:8000/api/ai/rewrite-text \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hey, can you check this out?",
    "style": "professional"
  }'
```

### 8. Extract Action Items

```bash
curl -X POST http://localhost:8000/api/ai/extract-action-items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Meeting notes: John will prepare slides by Friday. Sarah needs to review budget. Schedule follow-up next week."
  }'
```

### 9. Generate Email

```bash
curl -X POST http://localhost:8000/api/ai/generate-email \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "Request meeting with team",
    "key_points": [
      "Discuss Q1 roadmap",
      "Review user feedback",
      "Plan sprint"
    ],
    "tone": "professional"
  }'
```

### 10. Get AI Stats

```bash
curl -X GET http://localhost:8000/api/ai/stats \
  -H "Authorization: Bearer $TOKEN"
```

### 11. Conversation History

```bash
curl -X GET "http://localhost:8000/api/ai/conversations?limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🐍 Python Examples

### Setup

```python
import requests

BASE_URL = "http://localhost:8000"
TOKEN = "your_access_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
```

### Register & Login

```python
# Register
response = requests.post(
    f"{BASE_URL}/api/auth/signup",
    json={
        "email": "test@example.com",
        "password": "SecurePass123!",
        "full_name": "Test User"
    }
)
data = response.json()
TOKEN = data["access_token"]
```

### Create Task

```python
response = requests.post(
    f"{BASE_URL}/api/tasks",
    headers=headers,
    json={
        "title": "Build API endpoints",
        "priority": "high",
        "due_date": "2025-02-01T00:00:00Z"
    }
)
task = response.json()
print(f"Created task: {task['id']}")
```

### AI Chat

```python
response = requests.post(
    f"{BASE_URL}/api/ai/chat",
    headers=headers,
    json={
        "message": "Help me plan my day",
        "model": "gemini"
    }
)
result = response.json()
print(result["response"])
```

### Analyze Task

```python
response = requests.post(
    f"{BASE_URL}/api/ai/analyze-task",
    headers=headers,
    json={
        "task_title": "Build REST API",
        "task_description": "Create backend with FastAPI"
    }
)
analysis = response.json()
print(f"Estimated hours: {analysis['analysis']['estimated_hours']}")
print(f"Subtasks: {analysis['analysis']['subtasks']}")
```

---

## 📊 Complete Workflow Example

### Scenario: Project Planning with AI

```bash
# 1. Create a goal
GOAL_RESPONSE=$(curl -X POST http://localhost:8000/api/goals \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Launch Todo App",
    "priority": "high"
  }')

# 2. Generate AI plan for the goal
curl -X POST http://localhost:8000/api/ai/generate-goal-plan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal_title": "Launch Todo App",
    "target_date": "2025-06-01T00:00:00Z"
  }'

# 3. Create tasks from plan
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design database schema",
    "priority": "high"
  }'

# 4. Analyze each task
curl -X POST http://localhost:8000/api/ai/analyze-task \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_title": "Design database schema"
  }'

# 5. Track progress
curl -X PUT http://localhost:8000/api/tasks/{task_id} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

---

## 🧪 Testing Checklist

### Authentication
- [ ] Register new user
- [ ] Login existing user
- [ ] Refresh token
- [ ] Get user profile
- [ ] Update profile
- [ ] Change password
- [ ] Logout

### Goals
- [ ] Create goal
- [ ] List goals
- [ ] Get single goal
- [ ] Update goal
- [ ] Delete goal

### Tasks
- [ ] Create task
- [ ] List tasks
- [ ] Filter tasks (completed, priority)
- [ ] Update task
- [ ] Toggle completion
- [ ] Delete task

### Notes
- [ ] Create note
- [ ] List notes
- [ ] Search notes
- [ ] Update note
- [ ] Delete note

### Files
- [ ] Upload single file
- [ ] Upload multiple files
- [ ] List files
- [ ] Delete file

### AI Features
- [ ] General chat (Groq)
- [ ] General chat (Gemini)
- [ ] Task analysis
- [ ] Note summarization
- [ ] Goal planning
- [ ] Smart suggestions
- [ ] Brainstorming
- [ ] Text rewriting
- [ ] Action item extraction
- [ ] Email generation
- [ ] View conversations
- [ ] Get AI stats

---

## 🔍 Debugging Tips

### View Request/Response

```bash
# Add -v flag for verbose output
curl -v -X POST http://localhost:8000/api/ai/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Check Server Logs

```bash
# Server logs show all requests
python main.py
```

### Test in Browser

Open http://localhost:8000/api/docs for interactive testing

### Common Issues

**401 Unauthorized**
→ Token expired or invalid. Login again.

**422 Validation Error**
→ Check request body format

**500 Internal Server Error**
→ Check server logs for details

---

## 📝 Postman Collection

Import this into Postman:

```json
{
  "info": {
    "name": "Cosmic Assistant API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    },
    {
      "key": "token",
      "value": ""
    }
  ]
}
```

---

**Pro Tip**: Use the interactive docs at `/api/docs` for easiest testing!