from ipaddress import IPv4Address

from pydantic import BaseModel, Field


class Host(BaseModel):
    ip_address: IPv4Address
    mac_address: str = Field(pattern=r"^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    switch_id: str = Field(min_length=1)
    switch_port: int = Field(ge=1)