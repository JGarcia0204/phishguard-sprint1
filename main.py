
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3, os
from datetime import datetime

app = FastAPI(title="PhishGuard – Sprint 1 Demo")

DB_PATH = os.path.join(os.path.dirname(__file__), "sprint1.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        created_at TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        summary TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        note TEXT,
        created_at TEXT
    )""")
    cur.execute("SELECT COUNT(*) AS c FROM lessons")
    if cur.fetchone()["c"] == 0:
        cur.executemany("INSERT INTO lessons (title, summary) VALUES (?, ?)",
            [("Spotting Suspicious Links","Learn to hover and inspect URLs before clicking."),
             ("Sender Spoofing Basics","Identify odd domains and display-name tricks."),
             ("Attachments & Malware","Know when an attachment is risky.")])
    conn.commit(); conn.close()

init_db()

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

class UserIn(BaseModel):
    email: str
class ReportIn(BaseModel):
    source: str = "email"
    note: str = ""

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "PhishGuard – Sprint 1 Demo"})

@app.get("/lessons", response_class=HTMLResponse)
def lessons_page(request: Request):
    return templates.TemplateResponse("lessons.html", {"request": request, "title": "Lessons – PhishGuard"})

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "About – PhishGuard"})

@app.get("/api/lessons")
def api_lessons():
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id,title,summary FROM lessons")
    rows = [dict(r) for r in cur.fetchall()]; conn.close()
    return {"lessons": rows}

@app.post("/api/users")
def api_create_user(user: UserIn):
    conn = get_db(); cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (email, created_at) VALUES (?,?)",
                (user.email, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return {"status":"ok","email":user.email}

@app.post("/api/report")
def api_report(report: ReportIn):
    conn = get_db(); cur = conn.cursor()
    cur.execute("INSERT INTO reports (source,note,created_at) VALUES (?,?,?)",
                (report.source, report.note, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return {"status":"ok","message":"Report saved (Sprint 1 demo)."}

@app.get("/api/healthz")
def healthz():
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM lessons")
    c = cur.fetchone()["c"]; conn.close()
    return {"ok":True,"lessons_seeded":c}
