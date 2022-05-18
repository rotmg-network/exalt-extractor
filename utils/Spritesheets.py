import json
from utils.Logger import Logger

logger = Logger()


class Spritesheet:
    def __init__(self, sheet_name: str, atlas_id: int, elements: list):
        self.name = sheet_name
        self.atlas_id = atlas_id
        self.elements = elements


class SpritesheetParser:
    def __init__(self, sheet_data: bytes):
        self.data = str(sheet_data)
        self.sheet = json.loads(sheet_data)
        self.sprites = self.sheet["sprites"]
        self.animated_sprites = self.sheet["animatedSprites"]

        self.spritesheets = {}

        logger.info(f"loaded {len(self.sprites)} sprites")
        logger.info(f"loaded {len(self.animated_sprites)} animated sprites")
        self.parse_sheet()

    def parse_sheet(self):
        for sprite in self.sprites:
            sheet_name = sprite["spriteSheetName"]
            atlad_id = sprite["atlasId"]
            elements = sprite["elements"]

            if self.spritesheets.get(sheet_name) is None:
                sheet = Spritesheet(sheet_name, atlad_id, elements)
                self.spritesheets[sheet_name] = sheet

    def get_sheet_names(self):
        pass
