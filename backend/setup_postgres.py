"""
PostgreSQL Setup Script
Creates database and tables automatically
"""

import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from app.config import settings
from app.database import Base, engine
from app.models import orm_models  # Import all models


def create_database():
    """Create database if it doesn't exist"""
    print("=" * 60)
    print("POSTGRESQL DATABASE SETUP")
    print("=" * 60)
    print()
    
    # Extract database name from URL
    db_url = settings.DATABASE_URL
    db_name = db_url.split("/")[-1].split("?")[0]
    
    # Create connection to postgres database (not our app database)
    base_url = "/".join(db_url.split("/")[:-1]) + "/postgres"
    
    try:
        # Connect to default postgres database
        admin_engine = create_engine(base_url)
        
        with admin_engine.connect() as conn:
            # Need to commit immediately for CREATE DATABASE
            conn.execution_options(isolation_level="AUTOCOMMIT")
            
            # Check if database exists
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            )
            
            if result.fetchone():
                print(f"✅ Database '{db_name}' already exists")
            else:
                # Create database
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"✅ Database '{db_name}' created successfully")
        
        admin_engine.dispose()
        
    except OperationalError as e:
        print(f"❌ Could not connect to PostgreSQL: {e}")
        print()
        print("Make sure PostgreSQL is running:")
        print("  Windows: Check Services for PostgreSQL")
        print("  Mac: brew services start postgresql@15")
        print("  Linux: sudo systemctl start postgresql")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def create_tables():
    """Create all database tables"""
    print()
    print("Creating database tables...")
    print()
    
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Connected to database successfully")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print()
        print(f"✅ Created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        print()
        print("=" * 60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Start the server: python main.py")
        print("2. Visit: http://localhost:8000/api/docs")
        print("3. Test endpoints!")
        print()
        
    except OperationalError as e:
        print(f"❌ Could not connect to database: {e}")
        print()
        print("Check your .env file:")
        print(f"  DATABASE_URL={settings.DATABASE_URL}")
        print()
        print("Make sure:")
        print("  - PostgreSQL is running")
        print("  - Database exists")
        print("  - Username/password are correct")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


def verify_setup():
    """Verify database setup"""
    print()
    print("Verifying setup...")
    print()
    
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        # Check tables
        tables = inspector.get_table_names()
        expected_tables = ['users', 'goals', 'tasks', 'notes', 'files', 
                          'spreadsheets', 'ai_conversations', 'user_preferences', 
                          'activity_log']
        
        missing_tables = [t for t in expected_tables if t not in tables]
        
        if missing_tables:
            print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
        else:
            print("✅ All expected tables exist")
        
        # Check indexes
        print()
        print("Checking indexes...")
        for table in tables:
            indexes = inspector.get_indexes(table)
            if indexes:
                print(f"  {table}: {len(indexes)} indexes")
        
        print()
        print("✅ Verification complete!")
        
    except Exception as e:
        print(f"❌ Verification error: {e}")


def main():
    """Main setup function"""
    try:
        # Step 1: Create database
        create_database()
        
        # Step 2: Create tables
        create_tables()
        
        # Step 3: Verify setup
        verify_setup()
        
    except KeyboardInterrupt:
        print()
        print("Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()