import pytest
from pydantic import ValidationError

from src_controller.backend.models.firewall_rule import FirewallRule
from src_controller.backend.models.host import Host


def test_rule_rejects_destination_port_without_transport_protocol():
    with pytest.raises(ValidationError):
        FirewallRule(name="invalid port rule", destination_port=22)


def test_rule_accepts_tcp_port_and_timezone_aware_expiration():
    rule = FirewallRule(
        name="temporary ssh block",
        protocol="tcp",
        destination_port=22,
        expires_at="2030-01-01T12:00:00Z",
    )

    assert rule.destination_port == 22
    assert rule.expires_at is not None
    assert rule.expires_at.utcoffset().total_seconds() == 0


def test_rule_rejects_expiration_without_timezone():
    with pytest.raises(ValidationError):
        FirewallRule(name="temporary block", expires_at="2030-01-01T12:00:00")


def test_host_validates_mac_address():
    host = Host(
        ip_address="192.0.2.10",
        mac_address="00:11:22:33:44:55",
        switch_id="s1",
        switch_port=1,
    )

    assert host.mac_address == "00:11:22:33:44:55"

    with pytest.raises(ValidationError):
        Host(
            ip_address="192.0.2.10",
            mac_address="not-a-mac",
            switch_id="s1",
            switch_port=1,
        )
