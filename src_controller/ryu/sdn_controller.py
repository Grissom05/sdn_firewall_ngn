"""Small Ryu/OS-Ken OpenFlow 1.3 firewall controller for the Kathara lab."""

import logging
from collections import defaultdict
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import ClassVar, Optional

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import (
    CONFIG_DISPATCHER,
    DEAD_DISPATCHER,
    MAIN_DISPATCHER,
    set_ev_cls,
)
from ryu.lib.packet import ether_types, ethernet, packet
from ryu.ofproto import ofproto_v1_3

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class FirewallPolicy:
    """A simple IPv4 match that drops matching packets."""

    name: str
    source_ip: Optional[str] = None  # noqa: UP045
    destination_ip: Optional[str] = None  # noqa: UP045
    protocol: Optional[str] = None  # noqa: UP045
    destination_port: Optional[int] = None  # noqa: UP045
    priority: int = 100
    hard_timeout: int = 0

    def __post_init__(self):
        if self.protocol not in {None, "ip", "icmp", "tcp", "udp"}:
            raise ValueError(f"Unsupported IP protocol: {self.protocol}")
        if self.destination_port is not None:
            if self.protocol not in {"tcp", "udp"}:
                raise ValueError("destination_port requires tcp or udp")
            if not 1 <= self.destination_port <= 65535:
                raise ValueError("destination_port must be between 1 and 65535")
        for field_name in ("source_ip", "destination_ip"):
            address = getattr(self, field_name)
            if address is not None:
                IPv4Address(address)
        if not 1 <= self.priority <= 65535:
            raise ValueError("priority must be between 1 and 65535")
        if not 0 <= self.hard_timeout <= 65535:
            raise ValueError("hard_timeout must be between 0 and 65535")


# Example: deny traffic to TCP destination port 2020 for five minutes.
# Replace or extend this list with the policies needed by the lab.
FIREWALL_POLICIES = (
    FirewallPolicy(
        name="example-block-tcp-2020",
        protocol="tcp",
        destination_port=2020,
        hard_timeout=300,
    ),
)


class SDNFirewallController(app_manager.RyuApp):
    """Learning switch with higher-priority OpenFlow drop policies."""

    OFP_VERSIONS: ClassVar[list] = [ofproto_v1_3.OFP_VERSION]

    _IP_PROTOCOL_NUMBERS: ClassVar[dict] = {
        "icmp": 1,
        "tcp": 6,
        "udp": 17,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datapaths = {}
        self.mac_to_port = defaultdict(dict)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, event):
        datapath = event.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        self._install_firewall_policies(datapath)

        # Send packets without a matching flow to the controller.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER,
            )
        ]
        instructions = [
            parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)
        ]
        self._add_flow(datapath, priority=0, match=match, instructions=instructions)

        LOG.info("Installed table-miss and firewall policies on switch %016x", datapath.id)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def switch_state_change_handler(self, event):
        datapath = event.datapath
        if event.state == MAIN_DISPATCHER:
            self.datapaths[datapath.id] = datapath
            LOG.info("Switch %016x connected", datapath.id)
        elif event.state == DEAD_DISPATCHER:
            self.datapaths.pop(datapath.id, None)
            self.mac_to_port.pop(datapath.id, None)
            LOG.info("Switch %016x disconnected", datapath.id)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, event):
        message = event.msg
        datapath = message.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        dpid = datapath.id
        in_port = message.match["in_port"]

        parsed_packet = packet.Packet(message.data)
        ethernet_frame = parsed_packet.get_protocol(ethernet.ethernet)
        if ethernet_frame is None:
            return

        source_mac = ethernet_frame.src
        destination_mac = ethernet_frame.dst

        self.mac_to_port[dpid][source_mac] = in_port
        out_port = self.mac_to_port[dpid].get(destination_mac, ofproto.OFPP_FLOOD)
        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=destination_mac)
            instructions = [
                parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)
            ]
            self._add_flow(
                datapath,
                priority=1,
                match=match,
                instructions=instructions,
            )

        data = None
        if message.buffer_id == ofproto.OFP_NO_BUFFER:
            data = message.data

        packet_out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=message.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(packet_out)

    def _install_firewall_policies(self, datapath):
        parser = datapath.ofproto_parser
        for index, policy in enumerate(FIREWALL_POLICIES):
            match_fields = {"eth_type": ether_types.ETH_TYPE_IP}

            if policy.source_ip is not None:
                match_fields["ipv4_src"] = str(IPv4Address(policy.source_ip))
            if policy.destination_ip is not None:
                match_fields["ipv4_dst"] = str(IPv4Address(policy.destination_ip))

            if policy.protocol in self._IP_PROTOCOL_NUMBERS:
                match_fields["ip_proto"] = self._IP_PROTOCOL_NUMBERS[policy.protocol]
            if policy.destination_port is not None:
                match_fields[policy.protocol + "_dst"] = policy.destination_port

            match = parser.OFPMatch(**match_fields)
            self._add_flow(
                datapath,
                priority=policy.priority,
                match=match,
                instructions=[],
                cookie=0x53444E0000000000 + index,
                hard_timeout=policy.hard_timeout,
            )
            LOG.info(
                "Installed drop policy '%s' on switch %016x (timeout=%ss)",
                policy.name,
                datapath.id,
                policy.hard_timeout,
            )

    @staticmethod
    def _add_flow(
        datapath,
        priority,
        match,
        instructions,
        cookie=0,
        hard_timeout=0,
    ):
        message = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath,
            cookie=cookie,
            priority=priority,
            match=match,
            instructions=instructions,
            hard_timeout=hard_timeout,
        )
        datapath.send_msg(message)
