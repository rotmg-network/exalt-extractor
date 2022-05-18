from utils.Logger import Logger
from assets import TextAsset, Texture2D

logger = Logger()


class ActionScriptExtractor:
    def __init__(self, asset, output_path: str):
        self.output_path = output_path
        if isinstance(asset, TextAsset):
            self.asset = asset
            self.actionscript = self.parse_textasset()
        elif isinstance(asset, Texture2D):
            self.asset = asset
            self.actionscript = self.parse_texture2d()
        else:
            self.asset = None
            raise Exception("ActionScriptExtractor only supports TextAsset and Texture2D")

    def parse_texture2d(self) -> str:
        ret = "package kabam.rotmg.asset {{\n\n"
        ret += "\timport mx.core.BitmapAsset;\n\n"
        ret += f"\t[Embed(source=\"{self.asset.name}.png\")]\n"
        ret += f"\tpublic class {self.asset.name} extends BitmapAsset {{\n"
        ret += f"\t\tpublic function {self.asset.name}() {{\n"
        ret += "\t\t\tsuper();\n"
        ret += "\t\t}}\n\t}}\n}}"
        return ret

    def parse_textasset(self) -> str:
        ret = "package kabam.rotmg.asset {{\n\n"
        ret += "\timport mx.core.ByteArrayAsset;\n\n"
        ret += f"\t[Embed(source=\"{self.asset.name}.png\")]\n"
        ret += f"\tpublic class {self.asset.name} extends BitmapAsset {{\n"
        ret += f"\t\tpublic function {self.asset.name}() {{\n"
        ret += "\t\t\tsuper();\n"
        ret += "\t\t}}\n\t}}\n}}"
        return ret
