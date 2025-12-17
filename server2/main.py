from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path
import uvicorn

app = FastAPI()

DB_PATH = Path("db/shopping_list.json")

DB_BACKUP_PATH = Path("data/backup_shopping_list.json")

class Item(BaseModel):
    name: str
    quantity: int


def check_database_exists():
    if not DB_PATH.exists():
        print(f"ERROR: Database does not exist")
        raise FileNotFoundError(f"Database does not exist: {DB_PATH}")


def check_backup_database_exists():
    if not DB_BACKUP_PATH.exists():
        print(f"ERROR: Backup Database does not exist")
        raise FileNotFoundError(f"Backup Database does not exist: {DB_PATH}")


def load_database():
    with open(DB_PATH, "r") as f:
        return json.load(f)


def load_backup_database():
    with open(DB_BACKUP_PATH, "r") as f:
        return json.load(f)

def save_database(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

def save_backup_database(data):
    with open(DB_BACKUP_PATH, "w") as f:
        json.dump(data, f, indent=2)


@app.get("/items")
async def list_items():
    db = load_database()
    return db


@app.post("/items/")
async def create_item(item: Item):

    check_database_exists()

    db = load_database()
    item_id = len(db) + 1
    current_item = {"id": item_id, "name": item.name, "quantity": item.quantity}
    db.append(current_item)
    save_database(db)
    return {
        "message": "Item added successfully",
        "item_id": item_id,
        "item": current_item
            }


@app.get("/backup")
async def read_backup():
    db = load_backup_database()
    return db

@app.post("/backup/save")
def save_backup():
    check_database_exists()
    check_backup_database_exists()
    volume_db = load_database()
    save_backup_database(volume_db)
    return {
        "message": "Items backed up successfully",
        "Backup list": volume_db
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)