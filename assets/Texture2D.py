from utils.Logger import Logger

logger = Logger()

SPRITESHEET_NAMES = ["characters", "characters_masks", "groundTiles", "mapObjects"]

BG_PILLARS = "BGPillars"

PET_YARD = ["petYard_Rare", "petYard_Uncommon", "petYard_Legendary", "petYard_Divine"]
ARROWS = ["arrow_merchant_green", "arrow_merchant_red", "arrow_normal", "arrow_guild", "arrow_tell", "arrow_enemy"]
SPEECH = ["speech_merchant_green", "speech_merchant_red", "speech_normal", "speech_guild", "speech_tell", "speech_enemy"]
GUILD_ICONS = ["icon_guild_0", "icon_guild_10" "icon_guild_20", "icon_guild_30", "icon_guild_40"]
ICONS = ["clock_icon", "gold_icon", "fame_icon", "icon_lock", "icon_arrow", "icon_filter_consumables"]


class Texture2D:
    """ A wrapper around the Unity Texture2D resource type """

    def __init__(self, asset):
        try:
            self.data = asset
            self.name = asset.name
            self.image = asset.image
            self.image_data = asset.image_data
            self.width = asset.m_Width
            self.height = asset.m_Height
            self.size = asset.m_CompleteImageSize
            self.image_count = asset.m_ImageCount
            self.has_image = self.image_count > 0
        except Exception as e:
            self.data = None
            self.name = None
            logger.warn(f"Failed parsing Texture2D: {e}")
            print(f"{vars(asset)}\n")

    def __str__(self) -> str:
        if self.data is None:
            return ""
        ret = f"Name: {self.name}\nw: {self.width}px, h: {self.height}px\n"
        ret += f"Image Size: {self.size}\n"
        ret += f"Has Image: {self.has_image}\nImage Count: {self.image_count}\n"
        return ret

    def create_actionscript(self, file_type: str = "png", package_name: str = "kabam.rotmg.assets") -> str:
        """ Return a full ActionScript3 class file that will import the Texture2D image as a class """
        ret = f"package {package_name} {{\n\n"
        ret += "\timport mx.core.BitmapAsset;\n\n"
        ret += f"\t[Embed(source=\"{self.name}.{file_type}\")]\n"
        ret += f"\tpublic class {self.name} extends BitmapAsset {{\n"
        ret += f"\t\tpublic function {self.name}() {{\n"
        ret += "\t\t\tsuper();\n"
        ret += "\t\t}}\n\t}}\n}}"
        return ret

    @property
    def spritesheet(self) -> bool:
        """ Return True if the asset is used as a spritesheet file """
        return self.name in SPRITESHEET_NAMES
