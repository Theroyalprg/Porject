import sqlite3, json
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "inspections.sqlite3"
UPLOADS = ROOT / "data" / "uploads"
UPLOADS.mkdir(parents=True, exist_ok=True)

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, filename TEXT, image_path TEXT,
        asset_id TEXT, location TEXT, notes TEXT, review_status TEXT DEFAULT 'Pending review')""")

def save_inspection(filename, image_bytes, asset_id="", location="", notes=""):
    path = UPLOADS / f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{Path(filename).name}"
    path.write_bytes(image_bytes)
    with connect() as con:
        cur = con.execute("INSERT INTO inspections(created_at,filename,image_path,asset_id,location,notes) VALUES(?,?,?,?,?,?)",
          (datetime.now().astimezone().isoformat(timespec="seconds"), filename, str(path.relative_to(ROOT)), asset_id, location, notes))
        return cur.lastrowid

def list_inspections():
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT id,created_at,filename,asset_id,location,notes,review_status FROM inspections ORDER BY id DESC").fetchall()]

def update_review(record_id, status):
    with connect() as con:
        con.execute("UPDATE inspections SET review_status=? WHERE id=?", (status, record_id))
