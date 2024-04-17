from utils.Logger import Logger

logger = Logger()


class GameObject:
    """ A wrapper around the Unity GameObject resource type """

    def __init__(self, asset):
        try:
            self.data = asset
            self.name = asset.name
            self.components = asset.m_Components
            self.layer = asset.m_Layer
        except Exception as e:
            self.name = "Unknown"
            self.namespace = "Unknown"
            logger.warn(f"Failed parsing GameObject: {e}")
            # print(f"{vars(asset)}\n")
