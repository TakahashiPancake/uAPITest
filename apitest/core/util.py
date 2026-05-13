__all__ = ['safe_repr', 'IP', 'IPv6', 'TCP']

from unittest.util import safe_repr
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
from scapy.layers.inet6 import IPv6

