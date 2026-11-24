"""Ryu/OS-Ken application entry point.

The controller app will own switch event handling and translate firewall
policies into OpenFlow messages. It is intentionally not wired into the
Kathara startup script until that implementation is ready.
"""