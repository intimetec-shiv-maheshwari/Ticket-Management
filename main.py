from fastapi import FastAPI;
from src.routers.organizations import router as organizations_router;
from src.routers.users import router as users_router;
from src.routers.roles import router as roles_router;
from src.utils.db import init_db;

app = FastAPI(title="This is my Incident Management System");
init_db();
app.include_router(organizations_router);
app.include_router(users_router);
app.include_router(roles_router);
