from enum import Enum


class PacketTypes(Enum):
    INCOMING = "IncomingPacket"
    OUTGOING = "OutgoingPacket"
    DATA = "DataObjectPacket"


class AppEngineTypes(Enum):
    COMMANDS = "AppEngineCommand"
    MESSAGES = "AppEngineMessage"
    OUTGOING = "AppEngineOutgoing"
    XML = "AppEngineXML"


class OtherTypes(Enum):
    EFFECT = "Effect"
    PARTICLE = "Particle"
    MAP_OBJECT = "MapObject"
