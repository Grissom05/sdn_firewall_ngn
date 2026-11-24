from typing import NoReturn

from fastapi import HTTPException


def not_implemented(component: str) -> NoReturn:
    raise HTTPException(
        status_code=501,
        detail=f"{component} is not implemented yet.",
    )
