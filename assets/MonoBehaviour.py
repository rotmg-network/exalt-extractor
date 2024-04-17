from utils.Logger import Logger

logger = Logger()


class MonoBehaviour:
    """ A wrapper around the Unity MonoBehaviour resource type """

    def __init__(self, asset):
        try:
            self.data = asset
            self.name = asset.name
            self.script = asset.m_Script
            self.bytes = asset.raw_data
        except Exception as e:
            self.object_type = None
            self.name = "Unknown"
            self.namespace = "Unknown"
            logger.warn(f"Failed parsing MonoBehaviour: {e}")
            # print(f"{vars(asset)}\n")
