from os import mkdir
from os.path import exists, join


from utils.Logger import Logger
from utils import Resources, ActionScriptExtractor

logger = Logger()


def assert_path_exists(path: str) -> bool:
    if not exists(path):
        try:
            mkdir(path)
        except Exception as e:
            logger.error(f"Failed creating path '{path}': {e}")
            return False
    return True


class UnityExtractor:
    def __init__(self, resources: Resources, output_path: str):
        self.resources = resources
        self.output_path = output_path

    def extract_packets(self) -> None:
        """ Extract all outgoing, incoming and data object packet names from MonoScript assets """
        print()  # line break
        final_path = join(self.output_path, "packets")
        # ensure the 'packets' folder exists in the output directory
        if not exists(final_path):
            mkdir(final_path)

        logger.info(f"Extracting packet names to '{final_path}'...")
        out, inc, dat = [], [], []
        # iterate over all monoscript assets
        monoscript = self.resources.monoscripts
        for script in monoscript:
            if script.packet_outgoing:
                out.append(script.name)
            elif script.packet_incoming:
                inc.append(script.name)
            elif script.packet_data:
                dat.append(script.name)

        # sort the acquired lists A-Z
        out.sort(), inc.sort(), dat.sort()
        # log info about how many packets we extracted
        total = len(out) + len(inc) + len(dat)
        logger.info(f"Found {len(out)} outgoing, {len(inc)} incoming and {len(dat)} data object names ({total} total)")

        # write packet names to files
        with open(join(final_path, "outgoing.txt"), "w") as file:
            for name in out:
                file.write(f"{name}\n")
            logger.success("Saved 'packets/outgoing.txt' to the output folder.")
        with open(join(final_path, "incoming.txt"), "w") as file:
            for name in inc:
                file.write(f"{name}\n")
            logger.success("Saved 'packets/incoming.txt' to the output folder.")
        with open(join(final_path, "data.txt"), "w") as file:
            for name in dat:
                file.write(f"{name}\n")
            logger.success("Saved 'packets/data.txt' to the output folder.")

    def extract_xml(self, create_actionscript: bool = False) -> None:
        """ Extract all XML sheets from Unity TextAsset assets """
        print()  # line break
        final_path = join(self.output_path, "xml")
        # ensure the 'xml' folder exists in the output directory
        if not exists(final_path):
            mkdir(final_path)

        logger.info(f"Extracting XML files to '{final_path}'...")
        # iterate over every TextAsset asset
        sheets = self.resources.textassets
        sheet_count = 0
        for sheet in sheets:
            if not sheet.is_xml:
                continue
            with open(join(final_path, f"{sheet.name}.xml"), "wb") as file:
                file.write(sheet.file_data)
            if create_actionscript:
                # create an ActionScript3 class that imports the created .xml file
                with open(join(final_path, f"{sheet.name}.as"), "w") as file:
                    code = ActionScriptExtractor(sheet, final_path)
                    file.write(code.actionscript)
            sheet_count += 1

        # todo: consolidate objects, tiles and equips
        logger.success(f"Saved {sheet_count} XML files to the output folder.")
        if create_actionscript:
            logger.success(f"Created {sheet_count} matching ActionScript files to import the XML files.")

    def extract_spritesheets(self, create_actionscript: bool = False) -> None:
        print()  # line break
        final_path = join(self.output_path, "spritesheets")
        # ensure the 'spritesheets' folder exists in the output directory
        if not exists(final_path):
            mkdir(final_path)

        logger.info(f"Extracting spritesheets to '{final_path}'...")
        actionscript = {}

        sheets = self.resources.texture2ds
        for sheet in sheets:
            if not sheet.spritesheet:
                continue
            sheet.image.save(join(final_path, f"{sheet.name}.png"), "PNG")
            logger.success(f"Saved 'spritesheets/{sheet.name}.png' to the output folder.")
            if create_actionscript:
                code = ActionScriptExtractor(sheet, final_path)
                actionscript[sheet.name] = code.actionscript

        # optionally create ActionScript files that will import the .png file to a class
        for script in actionscript.keys():
            with open(join(final_path, f"{script}.as"), "w") as file:
                file.write(actionscript.get(script))
        if create_actionscript:
            logger.success(f"Created {len(actionscript)} ActionScript files to import the spritesheets.\n")

        spritesheet = self.resources.spritesheet
        with open(join(final_path, "spritesheet.json"), "wb") as file:
            file.write(spritesheet)
            logger.success("Saved 'spritesheets/spritesheet.json' to the output folder.")
        if create_actionscript:
            with open(join(final_path, "spritesheet.as"), "w") as file:
                # file.write()
                pass

    def extract_manifests(self) -> None:
        """ Extract the two asset manifest files """
        print()  # line break
        logger.info("Extracting the asset manifest files...")

        manifest = self.resources.manifest_json
        with open(join(self.output_path, "assets_manifest.json"), "wb") as file:
            file.write(manifest)
            logger.success("Saved 'assets_manifest.json' to the output folder.")

        manifest = self.resources.manifest_xml
        with open(join(self.output_path, "assets_manifest.xml"), "wb") as file:
            file.write(manifest)
            logger.success("Saved 'assets_manifest.xml' to the output folder.")

    def extract_texture2d(self) -> None:
        """ Save all parsed Texture2D assets to .png files """
        print()  # line break
        final_path = join(self.output_path, "texture2d")
        # ensure the 'texture2d' folder exists in the output directory
        if not assert_path_exists(final_path):
            logger.error("Could not extract Texture2D images to the output folder.")
            return
        logger.info(f"Extracting all Texture2D images to '{final_path}'...")

        textures = self.resources.texture2ds
        for texture in textures:
            if not texture.has_image:
                continue
