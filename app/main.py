import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, TESTING
from .routers import auth_routes, task_routes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AnythingAI Tasks API",
    version="1.0.0",
    description="Scalable REST API with authentication & role-based access for tasks.",
)

# CORS (allow frontend on same machine)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",  # e.g., Live Server or simple static host
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for assignment you can keep it open
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(task_routes.router)

# During pytest: reset DB once per test function so tests get isolated state
if TESTING:
    @app.middleware("http")
    async def reset_db(request, call_next):
        from . import database
        test_id = os.environ.get("PYTEST_CURRENT_TEST")
        if test_id:
            # normalize test id so fixture vs call use same base id
            base_test_id = test_id.split()[0]
            # debug
            print("DEBUG reset_db: test_id", test_id, "base", base_test_id, "last_test_id", database.last_test_id)
        else:
            base_test_id = None
        if base_test_id and database.last_test_id != base_test_id:
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            database.last_test_id = base_test_id
        response = await call_next(request)
        return response


@app.get("/health")
def health_check():
    return {"status": "ok"}
