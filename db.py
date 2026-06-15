import os
import ssl
from urllib.parse import urlparse
import pg8000
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        parsed = urlparse(db_url)
        port = parsed.port if parsed.port is not None else 5432
        
        # Enable SSL if connecting to an external database (not localhost)
        ssl_context = None
        if parsed.hostname not in ("localhost", "127.0.0.1") or "sslmode=require" in db_url:
            ssl_context = ssl.create_default_context()
            
        return pg8000.connect(
            host=parsed.hostname,
            database=parsed.path[1:],  # remove leading '/'
            user=parsed.username,
            password=parsed.password,
            port=port,
            ssl_context=ssl_context
        )
    
    # Fallback to individual credentials
    port_str = os.getenv("DB_PORT", "5432")
    return pg8000.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "hospital"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=int(port_str)
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id SERIAL PRIMARY KEY,
        patient_name VARCHAR(255) NOT NULL,
        phone VARCHAR(50) NOT NULL,
        appointment_date VARCHAR(50) NOT NULL,
        doctor VARCHAR(255) NOT NULL,
        symptoms TEXT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_all_as_dict(cursor):
    """
    Helper to convert standard pg8000 rows (tuples) into dictionaries.
    Required for rendering template properties (e.g. row.patient_name).
    """
    if not cursor.description:
        return []
    col_names = [desc[0] for desc in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor.fetchall()]

if __name__ == "__main__":
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
