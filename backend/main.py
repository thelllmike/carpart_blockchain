from fastapi import FastAPI
from model.database import engine, Base
from routers import users, parking

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(parking.router, prefix="/parking", tags=["parking"])
