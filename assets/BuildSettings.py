from utils.Logger import Logger

logger = Logger()


class BuildSettings:
    """ A wrapper around the Unity BuildSettings resource type """

    def __init__(self, asset):
        try:
            self.data = asset
            self.levels = asset.levels
            self.has_render_texture = asset.has_render_texture
            self.has_pro_version = asset.has_pro_version
            self.has_publishing_rights = asset.has_publishing_rights
            self.has_shadows = asset.has_shadows
        except Exception as e:
            self.data = None
            logger.warn(f"Failed parsing BuildSettings: {e}")
            logger.debug(f"{vars(asset)}\n")

    def __str__(self) -> str:
        if self.data is None:
            return ""
        ret = f"Levels: {self.levels}\nHas Render Texture: {self.has_render_texture}\n"
        ret += f"Pro Version: {self.has_pro_version}\nHas Publishing Rights: {self.has_publishing_rights}\n"
        ret += f"Has Shadows: {self.has_shadows}"
        return ret
