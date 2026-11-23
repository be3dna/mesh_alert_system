from enum import StrEnum


class NodeStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    CONNECTING = "connecting"
    LOW_POWER = "low_power"
