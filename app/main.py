from fastapi import FastAPI
from app.routes.research import router as research_router

app = FastAPI()

# Register the research router
app.include_router(research_router)

@app.get("/")
def read_root():
    return {"message": "Multi Agent AI Research System Backend Running"}
