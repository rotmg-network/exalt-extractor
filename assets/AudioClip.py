from utils.Logger import Logger

logger = Logger()


class AudioClip:
    """ A wrapper around the Unity AudioClip resource type """

    def __init__(self, asset):
        try:
            self.data = asset
            self.name = asset.name
            self.file_extension = asset.extension
            self.samples = asset.samples
        except Exception as e:
            self.data = None
            self.name = None
            logger.warn(f"Failed parsing BuildSettings: {e}")
            print(f"{vars(asset)}\n")

    def __str__(self) -> str:
        if self.data is None:
            return ""
        ret = f"Name: {self.name}\nFile extension: {self.file_extension}\n"
        ret += f"Sample Count: {len(self.samples)}\nSamples: {self.samples}"
        return ret
