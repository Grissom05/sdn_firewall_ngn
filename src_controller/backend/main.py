
from fastapi import FastAPI

app = FastAPI(
    title="SDN Firewall API",
    description="Backend per la gestione del firewall SDN",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "SDN Firewall Backend Online",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
