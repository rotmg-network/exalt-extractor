from .Enums import PacketTypes, AppEngineTypes, OtherTypes
from utils.Logger import Logger

logger = Logger()

# namespaces used in monoscript assets we need to parse
NAMESPACES = {
    "Packets": {
        "Incoming": "DecaGames.RotMG.Net.SocketServer.Messages.Incoming",
        "Outgoing": "DecaGames.RotMG.Net.SocketServer.Messages.Outgoing",
        "DataObject": "DecaGames.RotMG.Net.SocketServer.Messages.Data"
    },
    "AppEngine": {
        "Commands": "DecaGames.RotMG.Net.AppEngine.Commands",
        "Messages": "DecaGames.RotMG.Net.AppEngine.Messages",
        "Outgoing": "DecaGames.RotMG.Net.AppEngine.Outgoing",
        "XML": "DecaGames.RotMG.Net.AppEngine.XML.Serialization"
    },
    "Effects": "DecaGames.RotMG.Objects.Effects",
    "Particles": "DecaGames.RotMG.Objects.Particles",
    "MapObjects": "DecaGames.RotMG.Objects.Map"
}


class MonoScript:
    """ A wrapper around the Unity MonoScript resource type """

    def __init__(self, asset) -> None:
        try:
            self.data = asset
            self.namespace = asset.get("m_Namespace").strip()
            self.name = asset.get("m_ClassName")
            self.path_id = asset.get("path_id")
            self.unity_version = asset.get("version")
            self.object_type = self.parse_namespace()
        except Exception as e:
            self.object_type = None
            self.name = "Unknown"
            self.namespace = "Unknown"
            logger.warn(f"Failed parsing MonoScript: {e}")
            print(f"{vars(asset)}\n")

    def parse_namespace(self, namespace: str = None):
        """ determine the type of object by parsing the namespace """
        if namespace is None:
            namespace = self.namespace
        # _packets
        if NAMESPACES["Packets"]["Incoming"] in namespace:
            return PacketTypes.INCOMING
        elif NAMESPACES["Packets"]["Outgoing"] in namespace:
            return PacketTypes.OUTGOING
        elif namespace == NAMESPACES["Packets"]["DataObject"]:
            return PacketTypes.DATA
        # appengine data
        elif NAMESPACES["AppEngine"]["Commands"] in namespace:
            return AppEngineTypes.COMMANDS
        elif namespace == NAMESPACES["AppEngine"]["Messages"]:
            return AppEngineTypes.MESSAGES
        elif namespace == NAMESPACES["AppEngine"]["Outgoing"]:
            return AppEngineTypes.OUTGOING
        elif namespace == NAMESPACES["AppEngine"]["XML"]:
            return AppEngineTypes.XML
        # _particles / _effects
        elif namespace == NAMESPACES["Effects"]:
            return OtherTypes.EFFECT
        elif namespace == NAMESPACES["Particles"]:
            return OtherTypes.PARTICLE
        elif namespace == NAMESPACES["MapObjects"]:
            return OtherTypes.MAP_OBJECT
        return None

    @property
    def packet_incoming(self) -> bool:
        return self.object_type == PacketTypes.INCOMING

    @property
    def packet_outgoing(self) -> bool:
        return self.object_type == PacketTypes.OUTGOING

    @property
    def packet_data(self) -> bool:
        return self.object_type == PacketTypes.DATA

    @property
    def appengine_command(self) -> bool:
        return self.object_type == AppEngineTypes.COMMANDS

    @property
    def appengine_message(self) -> bool:
        return self.object_type == AppEngineTypes.MESSAGES

    @property
    def appengine_outgoing(self) -> bool:
        return self.object_type == AppEngineTypes.OUTGOING

    @property
    def appengine_xml(self) -> bool:
        return self.object_type == AppEngineTypes.XML

    @property
    def effect(self) -> bool:
        return self.object_type == OtherTypes.EFFECT

    @property
    def particle(self) -> bool:
        return self.object_type == OtherTypes.PARTICLE

    @property
    def map_object(self) -> bool:
        return self.object_type == OtherTypes.MAP_OBJECT
