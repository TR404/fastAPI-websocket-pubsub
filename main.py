#!/usr/bin/env python
from fastapi import FastAPI

from app import views 
from settings.database import Base, engine

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(views.router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
