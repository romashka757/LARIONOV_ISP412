from typing import Dict, List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Item


app = FastAPI(title="ISP-412 Alt API", version="1.0.0")

# Static and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# Create tables on startup
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/items", response_model=List[Dict[str, str]])
async def list_items(db: Session = Depends(get_db)) -> List[Dict[str, str]]:
    rows = db.query(Item).all()
    return [
        {"id": str(row.id), "name": row.name, "description": row.description}
        for row in rows
    ]


@app.post("/api/items", status_code=201)
async def create_item(item: Dict[str, str], db: Session = Depends(get_db)) -> Dict[str, str]:
    if not item.get("name"):
        raise HTTPException(status_code=400, detail="'name' is required")
    row = Item(name=item["name"], description=item.get("description", ""))
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": str(row.id), "name": row.name, "description": row.description}


@app.get("/api/items/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)) -> Dict[str, str]:
    row = db.get(Item, item_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": str(row.id), "name": row.name, "description": row.description}


@app.put("/api/items/{item_id}")
async def update_item(item_id: int, item: Dict[str, str], db: Session = Depends(get_db)) -> Dict[str, str]:
    row = db.get(Item, item_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if not item.get("name"):
        raise HTTPException(status_code=400, detail="'name' is required")
    row.name = item["name"]
    row.description = item.get("description", "")
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": str(row.id), "name": row.name, "description": row.description}


@app.delete("/api/items/{item_id}", status_code=204)
async def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    row = db.get(Item, item_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(row)
    db.commit()
    return None


