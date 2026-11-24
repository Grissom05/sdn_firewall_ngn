from fastapi import APIRouter

from ._placeholder import not_implemented

router = APIRouter(tags=["Monitoring"])


@router.get("/stats")
def get_statistics():
    not_implemented("Traffic statistics")


@router.get("/flows")
def list_flows():
    not_implemented("Installed OpenFlow rules")