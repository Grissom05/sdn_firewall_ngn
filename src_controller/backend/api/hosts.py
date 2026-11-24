from fastapi import APIRouter

from ._placeholder import not_implemented

router = APIRouter(tags=["Hosts"])


@router.get("/")
def list_hosts():
    not_implemented("Host discovery")