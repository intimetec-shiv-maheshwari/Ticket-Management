from fastapi import FastAPI;
from src.routers.organizations import router as organizations_router;
from src.utils.db import init_db;

app = FastAPI(title="This is my Incident Management System");
init_db();
app.include_router(organizations_router);
