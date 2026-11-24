
from fastapi import FastAPI

from .api.firewall import router as firewall_router
from .api.hosts import router as hosts_router
from .api.monitoring import router as monitoring_router

app = FastAPI(
    title="SDN Firewall API",
    description="API di amministrazione per il firewall SDN",
    version="0.1.0",
)

app.include_router(firewall_router, prefix="/api/v1/firewall")
app.include_router(hosts_router, prefix="/api/v1/hosts")
app.include_router(monitoring_router, prefix="/api/v1/monitoring")


@app.get("/")
def home():
    return {
        "message": "SDN Firewall Backend Online",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
