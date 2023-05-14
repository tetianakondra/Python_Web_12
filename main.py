import time

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.db import get_db
from src.routes import contacts, auth

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    print(request.client)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["performance"] = str(process_time)
    return response

@app.get("/")
def read_root():
    return {"message": "Hello, this is HW12"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix='/api')
