from fastapi import FastAPI
from approval.api import router

app = FastAPI(title="青阳云审批集成服务")

app.include_router(router, prefix="/api/approval")


@app.get("/health")
def health_check():
    return {"status": "ok"}
