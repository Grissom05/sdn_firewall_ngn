from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address

from pydantic import BaseModel, Field, field_validator, model_validator


class FirewallProtocol(str, Enum):
    IP = "ip"
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"


class FirewallAction(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


class TrafficDirection(str, Enum):
    INGRESS = "ingress"
    EGRESS = "egress"
    BOTH = "both"


class FirewallRule(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    source_ip: IPv4Address | None = None
    destination_ip: IPv4Address | None = None
    protocol: FirewallProtocol | None = None
    destination_port: int | None = Field(default=None, ge=1, le=65535)
    direction: TrafficDirection = TrafficDirection.BOTH
    action: FirewallAction = FirewallAction.DENY
    enabled: bool = True
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def validate_port_protocol(self):
        if self.destination_port is not None and self.protocol not in {
            FirewallProtocol.TCP,
            FirewallProtocol.UDP,
        }:
            raise ValueError("destination_port requires TCP or UDP protocol")
        return self

    @field_validator("expires_at")
    @classmethod
    def require_timezone_on_expiration(cls, value: datetime | None):
        if value is not None and value.utcoffset() is None:
            raise ValueError("expires_at must include a timezone")
        return value