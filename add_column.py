from app import app, db
from sqlalchemy import text  # <-- Add this import

with app.app_context():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE user_info ADD COLUMN user_type VARCHAR(50) DEFAULT 'user';
            """))  # <-- wrap with text()
            print("user_type column added to user_info!")
    except Exception as e:
        print("Error adding column:", e)
