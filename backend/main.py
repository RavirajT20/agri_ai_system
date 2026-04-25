from fastapi import FastAPI
from api import education_routes, triage_routes

app = FastAPI(title="Agri AI System")

app.include_router(education_routes.router, prefix="/education")
app.include_router(triage_routes.router, prefix="/triage")