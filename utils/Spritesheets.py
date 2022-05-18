import json

from utils.Logger import Logger

logger = Logger()


class Spritesheet:
    """ A class representation of the Unity Spritesheet asset object """

    def __init__(self, sheet_name: str, atlas_id: int, elements: list):
        self.name = sheet_name
        self.atlas_id = atlas_id
        self.elements = elements


class SpritesheetParser:
    """ A class that will parse the 'spritesheet.json' file designed for a Unity SpriteAtlas """

    def __init__(self, sheet_data: bytes):
        self.data = str(sheet_data)
        # load the json data into a python object
        self.sheet = json.loads(sheet_data)
        self.sprites = self.sheet["sprites"]
        self.animated_sprites = self.sheet["animatedSprites"]

        self.spritesheets = {}

        logger.info(f"Loaded {len(self.sprites)} sprites.")
        logger.info(f"Loaded {len(self.animated_sprites)} animated sprites.")
        # finally parse the whole spritesheet
        self.parse_sheet()

    def parse_sheet(self):
        """ Extracts all sprites and animated sprite objects from the spritesheet file """
        for sprite in self.sprites:
            sheet_name = sprite["spriteSheetName"]
            atlas_id = sprite["atlasId"]
            elements = sprite["elements"]

            if self.spritesheets.get(sheet_name) is None:
                sheet = Spritesheet(sheet_name, atlas_id, elements)
                self.spritesheets[sheet_name] = sheet

    def get_spritesheets(self) -> list[Spritesheet]:
        """ Return all parsed Spritesheet objects """

    def get_sheet_names(self) -> list[str]:
        """ Return a list of all parsed spritesheets from the SpriteAtlas """
        pass
