from uuid import UUID

from fastapi import APIRouter

from ..models.firewall_rule import FirewallRule
from ._placeholder import not_implemented

router = APIRouter(tags=["Firewall rules"])


@router.get("/rules")
def list_rules():
    not_implemented("Listing firewall rules")


@router.post("/rules", status_code=201)
def create_rule(rule: FirewallRule):
    not_implemented("Creating and installing firewall rules")


@router.patch("/rules/{rule_id}")
def update_rule(rule_id: UUID, rule: FirewallRule):
    not_implemented("Updating firewall rules")


@router.delete("/rules/{rule_id}", status_code=204)
def delete_rule(rule_id: UUID):
    not_implemented("Removing firewall rules")