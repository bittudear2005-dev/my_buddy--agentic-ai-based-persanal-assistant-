# 🎯 Complete PostgreSQL Setup - Step by Step

## 📦 **What You're Getting**

✅ PostgreSQL database instead of Supabase  
✅ SQLAlchemy ORM for database operations  
✅ Local authentication with JWT  
✅ All AI features (unchanged)  
✅ Better control and no vendor lock-in  

---

## 🚀 **Quick Start (5 Steps)**

### **Step 1: Install PostgreSQL**

**Windows:**
1. Download: https://www.postgresql.org/download/windows/
2. Run installer
3. Set password for `postgres` user (remember this!)
4. Keep default port: 5432
5. Install pgAdmin 4 (optional GUI)

**Mac:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux:**
```bash
sudo apt update
sudo apt install postgresql
sudo systemctl start postgresql
```

---

### **Step 2: Install Python Dependencies**

```bash
cd D:\PA\workmate\backend

# Remove old Supabase packages
pip uninstall supabase postgrest -y

# Install new packages
pip install -r requirements.txt
```

**New packages include:**
- `sqlalchemy` - Database ORM
- `psycopg2-binary` - PostgreSQL driver
- `alembic` - Database migrations
- `passlib` - Password hashing

---

### **Step 3: Update Configuration**

**Copy new `.env.example` to `.env` and update:**

```bash
# CRITICAL: Update these lines
database_url=postgresql://postgres:YOUR_PASSWORD@localhost:5432/cosmic_assistant

# Keep your AI API keys
groq_api_key=gsk_xxxxx
gemini_api_key=AIzaSyxxxxx

# Generate new secret key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
secret_key=your-new-secret-key-here
```

---

### **Step 4: Create All New Files**

**NEW FILES to create:**

1. ✅ `app/database.py` - Database connection
2. ✅ `app/models/orm_models.py` - SQLAlchemy models
3. ✅ `setup_postgres.py` - Database setup script

**FILES to UPDATE:**

4. ✅ `app/config.py` - PostgreSQL configuration
5. ✅ `app/routes/auth.py` - New authentication
6. ✅ `app/routes/goals.py` - SQLAlchemy version
7. ✅ `main.py` - Updated for PostgreSQL

**KEEP AI FILES (no changes needed):**
- ✅ `app/services/ai_service.py` - No changes
- ✅ `app/models/database.py` - No changes (Pydantic models)

All file contents are in the **artifacts above** ⬆️

---

### **Step 5: Setup Database and Run**

```bash
# Setup database (creates database + tables)
python setup_postgres.py

# Start server
python main.py
```

Visit: http://localhost:8000/api/docs 🎉

---

## 📁 **Complete File List**

### **Files from Artifacts (Copy These):**

| Priority | File | Artifact Name | Size |
|----------|------|---------------|------|
| 🔴 HIGH | `requirements.txt` | "requirements.txt - PostgreSQL Version" | Small |
| 🔴 HIGH | `app/config.py` | "app/config.py - PostgreSQL Configuration" | Medium |
| 🔴 HIGH | `app/database.py` | "app/database.py - Database Connection" | Small |
| 🔴 HIGH | `app/models/orm_models.py` | "app/models/orm_models.py - SQLAlchemy ORM Models" | Large |
| 🔴 HIGH | `app/routes/auth.py` | "app/routes/auth.py - PostgreSQL Authentication" | Large |
| 🔴 HIGH | `app/routes/goals.py` | "app/routes/goals.py - PostgreSQL Version" | Medium |
| 🔴 HIGH | `main.py` | "main.py - PostgreSQL Version" | Small |
| 🔴 HIGH | `setup_postgres.py` | "setup_postgres.py - Database Setup Script" | Medium |
| 🟡 MED | `.env.example` | ".env.example - PostgreSQL Version" | Small |

### **Keep These Files (No Changes):**

| File | Status |
|------|--------|
| `app/services/ai_service.py` | ✅ Keep unchanged |
| `app/models/database.py` | ✅ Keep unchanged (Pydantic models) |
| `app/services/__init__.py` | ✅ Keep unchanged |
| `app/models/__init__.py` | ✅ Keep unchanged |

### **Update These Files (Similar to goals.py):**

| File | Action | Priority |
|------|--------|----------|
| `app/routes/notes.py` | Update queries to SQLAlchemy | 🟡 Medium |
| `app/routes/tasks.py` | Update queries to SQLAlchemy | 🟡 Medium |
| `app/routes/files.py` | Update storage to local | 🟡 Medium |
| `app/routes/spreadsheets.py` | Update queries to SQLAlchemy | 🟡 Medium |
| `app/routes/ai_chat.py` | Update conversation queries | 🟢 Low |

**Pattern:** Follow the same pattern as `goals.py` - Replace Supabase queries with SQLAlchemy queries.

---

## 🔄 **Migration Pattern**

### **Example: Update any route file**

**OLD (Supabase):**
```python
from supabase import create_client
supabase = create_client(url, key)

response = supabase.table("notes").select("*").eq("user_id", user_id).execute()
notes = response.data
```

**NEW (SQLAlchemy):**
```python
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orm_models import Note

notes = db.query(Note).filter(Note.user_id == user_id).all()
```

**Key Changes:**
1. Replace `supabase.table("notes")` with `db.query(Note)`
2. Replace `.eq()` with `.filter()`
3. Replace `.execute().data` with `.all()` or `.first()`
4. Add `db: Session = Depends(get_db)` to function parameters

---

## ✅ **Verification Checklist**

After setup, verify:

```bash
# 1. Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# 2. Check database exists
psql -U postgres -c "\l" | grep cosmic_assistant

# 3. Check tables were created
python setup_postgres.py

# 4. Start server
python main.py

# Should see:
# ✅ Database tables created/verified
# INFO: Uvicorn running on http://0.0.0.0:8000
```

**Test in browser:**
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/api/docs

**Test registration:**
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "full_name": "Test User"
  }'
```

Should return `access_token` ✅

---

## 🆘 **Common Issues & Solutions**

### **Issue 1: "could not connect to server"**
```
OperationalError: could not connect to server
```
**Solution:**
- PostgreSQL is not running
- Windows: Start PostgreSQL service
- Mac: `brew services start postgresql@15`
- Linux: `sudo systemctl start postgresql`

---

### **Issue 2: "password authentication failed"**
```
OperationalError: password authentication failed
```
**Solution:**
- Wrong password in `.env`
- Update DATABASE_URL with correct password
```bash
database_url=postgresql://postgres:CORRECT_PASSWORD@localhost:5432/cosmic_assistant
```

---

### **Issue 3: "database does not exist"**
```
OperationalError: database "cosmic_assistant" does not exist
```
**Solution:**
- Run setup script: `python setup_postgres.py`
- OR manually: `psql -U postgres -c "CREATE DATABASE cosmic_assistant;"`

---

### **Issue 4: "relation does not exist"**
```
ProgrammingError: relation "users" does not exist
```
**Solution:**
- Tables not created
- Run: `python setup_postgres.py`

---

### **Issue 5: ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'sqlalchemy'
```
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 🎯 **Priority Action Plan**

### **Phase 1: Critical (Do First)**
1. ✅ Install PostgreSQL
2. ✅ Install Python packages: `pip install -r requirements.txt`
3. ✅ Create `app/database.py`
4. ✅ Create `app/models/orm_models.py`
5. ✅ Update `app/config.py`
6. ✅ Update `.env` file
7. ✅ Create `setup_postgres.py`
8. ✅ Run: `python setup_postgres.py`

### **Phase 2: Essential (Do Next)**
9. ✅ Update `app/routes/auth.py`
10. ✅ Update `app/routes/goals.py`
11. ✅ Update `main.py`
12. ✅ Test: `python main.py`

### **Phase 3: Completion (Do Later)**
13. 🟡 Update `app/routes/notes.py` (follow goals.py pattern)
14. 🟡 Update `app/routes/tasks.py` (follow goals.py pattern)
15. 🟡 Update `app/routes/files.py` (local storage)
16. 🟡 Update `app/routes/spreadsheets.py` (follow goals.py pattern)
17. 🟡 Minor updates to `app/routes/ai_chat.py`

---

## 💡 **Pro Tips**

1. **Start Small**
   - Get auth working first
   - Then goals
   - Then other routes

2. **Use pgAdmin**
   - Visual database management
   - Easier to debug issues
   - Can see all tables/data

3. **Test Each Change**
   - Test auth → Test goals → Test notes → etc.
   - Don't change everything at once

4. **Backup Often**
   ```bash
   pg_dump cosmic_assistant > backup.sql
   ```

5. **Use Database Migrations** (Later)
   ```bash
   alembic init alembic
   alembic revision --autogenerate -m "Add column"
   alembic upgrade head
   ```

---

## 📚 **Resources**

- **PostgreSQL Tutorial**: https://www.postgresqltutorial.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **FastAPI + SQLAlchemy**: https://fastapi.tiangolo.com/tutorial/sql-databases/
- **pgAdmin 4**: https://www.pgadmin.org/

---

## 🎉 **You're Ready!**

All the code is in the artifacts above. Just:

1. Copy each file from artifacts
2. Update your `.env`
3. Run `python setup_postgres.py`
4. Run `python main.py`
5. Visit http://localhost:8000/api/docs

**The AI features remain completely unchanged!** 🤖

---

**Questions? Check MIGRATION_GUIDE.md for detailed explanations!**