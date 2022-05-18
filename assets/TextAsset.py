from utils.Logger import Logger

logger = Logger()

# list of all filenames that do not contain XML content
NON_XML_FILES = [
    "manifest_xml", "COPYING", "Errors", "ExplainUnzip", "cloth_bazaar", "Cursors", "Dialogs", "Keyboard",
    "LICENSE", "LineBreaking Following Characters", "LineBreaking Leading Characters", "manifest_json", "spritesheet",
    "iso_4217", "data"
]


class TextAsset:
    """ A wrapper around the Unity TextAsset resource type """

    def __init__(self, asset):
        try:
            self.data = asset
            self.name = asset.get("name")
            self.path_id = asset.get("path_id")
            self.file_data = asset.script
        except Exception as e:
            self.data, self.name = None, None
            logger.error(f"Error loading TextAsset: {e}")
            print(f"{vars(asset)}\n")

    def create_actionscript(self, file_type: str = "xml", package_name: str = "kabam.rotmg.assets") -> str:
        """ Return a full ActionScript3 class file that will import the TextAsset as a class """
        ret = f"package {package_name} {{\n\n"
        ret += "\timport mx.core.ByteArrayAsset;\n\n"
        ret += f"\t[Embed(source=\"{self.name}.{file_type}\", mimeType=\"application/octet-stream\")]\n"
        ret += f"\tpublic class {self.name} extends ByteArrayAsset {{\n"
        ret += f"\t\tpublic function {self.name}() {{\n"
        ret += "\t\t\tsuper();\n"
        ret += "\t\t}}\n\t}}\n}}"
        return ret

    @property
    def is_xml(self) -> bool:
        return self.name is not None and self.name not in NON_XML_FILES

    @property
    def spritesheet(self) -> bool:
        return self.name == "spritesheet"

    @property
    def manifest_json(self) -> bool:
        return self.name == "manifest"

    @property
    def manifest_xml(self) -> bool:
        return self.name == "assets_manifest"
