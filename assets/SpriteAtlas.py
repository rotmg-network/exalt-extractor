from utils.Logger import Logger

logger = Logger()


class SpriteAtlas:
    """ A wrapper around the Unity SpriteAtlas resource type """

    def __init__(self, asset):
        try:
            self.data = asset
            self.name = asset.name
            self.packed_sprites = asset.m_PackedSprites  # list of Sprite assets
            self.packed_sprite_names = asset.m_PackedSpriteNamesToIndex
            self.render_data_map = asset.m_RenderDataMap  # list of SpriteAtlasData objects
        except Exception as e:
            self.data = None
            self.name = None
            logger.warn(f"Failed parsing SpriteAtlas: {e}")
            # print(f"{vars(asset)}\n")

    def __str__(self) -> str:
        if self.data is None:
            return ""
        ret = f"Packed Sprites: {self.packed_sprites}\n\n"
        ret += f"Packed Sprite Names: {self.packed_sprite_names}\n\n"
        # ret += f"Render Data Map: {self.render_data_map}" # todo: uncomment
        return ret


class SpriteAtlasData:
    # todo: finish this class
    def __init__(self):
        pass
