from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "notesdb")
DB_USER = os.getenv("DB_USER", "notesuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


class Note(BaseModel):
    message: str


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/notes")
def create_note(note: Note):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (message) VALUES (%s) RETURNING id",
        (note.message,)
    )
    note_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"id": note_id, "message": note.message}


@app.get("/notes")
def get_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, message FROM notes ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{"id": row[0], "message": row[1]} for row in rows]
