import UnityPy
import pathlib
from os import walk
from os.path import join, exists
from getpass import getuser
from platform import system
from sys import exit as exit_program

from assets import AudioClip, BuildSettings, GameObject, TextAsset, Texture2D, SpriteAtlas, MonoScript, MonoBehaviour

from utils.Logger import Logger, get_input

logger = Logger()

# the default path for the Exalt Unity resources on all default Windows installs
PATH_WINDOWS = join("Documents", "RealmOfTheMadGod", "Production", "RotMG Exalt_Data")
# the default path for the Exalt Unity resources on all default macOS installs
PATH_MACOS = join("RealmOfTheMadGod", "Production", "RotMGExalt.app", "Contents", "Resources", "Data")


def get_resource_path() -> str:
    """ Attempt to automatically find the Exalt resource path based on OS and the current user """
    operating_sys = system()
    path = ""
    if operating_sys == "Windows":
        logger.info("Detected Windows operating system.")
        path = pathlib.Path(join(pathlib.Path.home(), PATH_WINDOWS))
    elif operating_sys == "Darwin":
        logger.info("Detected MacOS operating system.")
        path = join(pathlib.Path.home(), PATH_MACOS)
    else:
        logger.critical(f"Unsupported operating system '{operating_sys}'... only Windows and MacOS are supported")
        print()  # line break
        exit_program(1)

    if not exists(path):
        # ask the user to input the Exalt path manually as a fallback
        path = pathlib.Path(get_path_input())
        logger.success("Found valid Exalt resource path\n")
    else:
        logger.success(f"Found Exalt resource path: {path}")
    return path


def get_path_input() -> str:
    """ Attempt to get a game resource path from console input or exit """
    print()  # line break
    logger.error("Could not find the Exalt resource path automatically... is Exalt installed?")

    operating_sys = system()
    if operating_sys == "Windows":
        logger.error(f"The path is usually located here: C:\\Users\\{getuser()}\\{PATH_WINDOWS}\n")
    elif operating_sys == "Darwin":
        logger.error(f"The path is usually located here: /Users/{getuser()}/{PATH_MACOS}\n")

    # loop asking for a path input until the user exits
    path = ""
    while path == "":
        input_path = get_input("Enter your resource path manually or press the Enter key to exit")
        print()  # line break
        if input_path == "":
            logger.success("Exiting...")
            exit_program(0)
        if exists(input_path):
            if not exists(join(input_path, "resources.assets")):
                logger.error(f"Invalid path - no 'resources.assets' file in directory: {input_path}")
                print()  # line break
            else:
                path = input_path
                break  # break if we get a valid directory
        else:
            logger.error(f"Invalid path - could not find directory: {input_path}")
            print()  # line break
    return path


class Resources:
    """ This class will automatically parse all Unity assets from the game directory files into classes """

    def __init__(self, resource_path=None):
        if resource_path is None:
            # try to find the Exalt resource path depending on the OS
            self.path = get_resource_path()
        else:
            self.path = resource_path
        # walk through all files in the path and parse any Unity asset files
        self.resource_files = self.parse_all_files()
        # initialize lists for all types of parsed assets
        self.all_resources = {
            "AudioClip": [], "BuildSettings": [], "GameObject": [], "MonoBehaviour": [],
            "MonoScript": [], "SpriteAtlas": [], "TextAsset": [], "Texture2D": []
        }
        # initialize lists of packet name types
        self._packets = {"incoming": [], "outgoing": [], "data": []}
        # initialize lists of other names
        self._effects, self._particles, self._map_objects = [], [], []
        self._spritesheet = None
        self._manifest_json, self._manifest_xml = None, None
        # parse all assets
        self.parse_all_resources()

    def parse_all_files(self) -> list:
        """ Returns a list of all parsed resource files from the game directory """
        all_files = []
        for root, _, files in walk(self.path):
            for file_name in files:
                all_files.append(UnityPy.load(join(root, file_name)))
        return all_files

    def parse_all_resources(self) -> None:
        """ Iterate over each resource file and return certain types of objects """
        res_count = 0
        for res in self.resource_files:
            for obj in res.objects:
                if obj.type.name == "AudioClip":
                    # self.parse_audioclip(obj)
                    pass
                elif obj.type.name == "BuildSettings":
                    self.parse_buildsettings(obj)
                elif obj.type.name == "GameObject":
                    self.parse_gameobject(obj)
                elif obj.type.name == "TextAsset":
                    self.parse_textasset(obj)
                elif obj.type.name == "SpriteAtlas":
                    self.parse_spriteatlas(obj)
                elif obj.type.name == "MonoScript":
                    self.parse_monoscript(obj)
                elif obj.type.name == "Texture2D":
                    self.parse_texture2d(obj)
                elif obj.type.name == "MonoBehaviour":
                    self.parse_monobehaviour(obj)
                else:
                    continue
                res_count += 1
        # sort all parsed objects A-Z
        # self._packets["outgoing"].sort(), self._packets["incoming"].sort(), self._packets["data"].sort()
        self._effects.sort(), self._particles.sort(), self._map_objects.sort()
        logger.success(f"Parsed {res_count} total assets!")

    def parse_audioclip(self, obj) -> None:
        """ Read a AudioClip asset object and append to the tracked assets """
        asset = AudioClip(obj.read())
        self.all_resources["AudioClip"].append(asset)

    def parse_buildsettings(self, obj) -> None:
        """ Read a BuildSettings asset object and append to the tracked assets """
        asset = BuildSettings(obj.read())
        self.all_resources["BuildSettings"].append(asset)

    def parse_gameobject(self, obj) -> None:
        """ Read a GameObject asset object and append to the tracked assets """
        asset = GameObject(obj.read())
        self.all_resources["GameObject"].append(asset)

    def parse_monobehaviour(self, obj) -> None:
        """ Read a MonoBehaviour asset object and append to the tracked assets """
        asset = MonoBehaviour(obj.read())
        self.all_resources["MonoBehaviour"].append(asset)

    def parse_monoscript(self, obj) -> None:
        """ Read a MonoScript asset object and append to the tracked assets """
        asset = MonoScript(obj.read())
        # _packets
        if asset.packet_outgoing:
            self._packets["outgoing"].append(asset)
        elif asset.packet_incoming:
            self._packets["incoming"].append(asset)
        elif asset.packet_data:
            self._packets["data"].append(asset)
        # misc types
        elif asset.effect:
            self._effects.append(asset.name)
        elif asset.particle:
            self._particles.append(asset.name)
        elif asset.map_object:
            self._map_objects.append(asset.name)
        self.all_resources["MonoScript"].append(asset)

    def parse_spriteatlas(self, obj) -> None:
        """ Read a SpriteAtlas asset object and append to the tracked assets """
        asset = SpriteAtlas(obj.read())
        self.all_resources["SpriteAtlas"].append(asset)

    def parse_textasset(self, obj) -> None:
        """ Read a TextAsset asset object and append to the tracked assets """
        asset = TextAsset(obj.read())
        if asset.spritesheet:
            self._spritesheet = asset.file_data
        if asset.manifest_json:
            self._manifest_json = asset.file_data
        if asset.manifest_xml:
            self._manifest_xml = asset.file_data
        self.all_resources["TextAsset"].append(asset)

    def parse_texture2d(self, obj) -> None:
        """ Read a Texture2D asset object and append to the tracked assets """
        asset = Texture2D(obj.read())
        self.all_resources["Texture2D"].append(asset)

    @property
    def spritesheet(self) -> bytes:
        """ Return the 'spritesheet.json' file data"""
        return self._spritesheet

    @property
    def manifest_json(self) -> bytes:
        """ Return the JSON asset manifest file data """
        return self._manifest_json

    @property
    def manifest_xml(self) -> bytes:
        """ Return the XML asset manifest file data """
        return self._manifest_xml

    @property
    def effects(self) -> list:
        """ Return a list of all effect names """
        return self._effects

    @property
    def particles(self) -> list:
        """ Return a list of all particle names """
        return self._particles

    @property
    def map_objects(self) -> list:
        """ Return a list of all map object names """
        return self._map_objects

    @property
    def audioclips(self) -> list[AudioClip]:
        """ Returns all parsed AudioClip assets """
        return self.all_resources["AudioClip"]

    @property
    def buildsettings(self) -> list[BuildSettings]:
        """ Returns all parsed BuildSettings assets """
        return self.all_resources["BuildSettings"]

    @property
    def gameobjects(self) -> list[GameObject]:
        """ Returns all parsed GameObject assets """
        return self.all_resources["GameObject"]

    @property
    def textassets(self) -> list[TextAsset]:
        """ Returns all parsed TextAsset assets """
        return self.all_resources["TextAsset"]

    @property
    def texture2ds(self) -> list[Texture2D]:
        """ Returns all parsed Texture2D assets """
        return self.all_resources["Texture2D"]

    @property
    def spriteatlases(self) -> list[SpriteAtlas]:
        """ Returns all parsed SpriteAtlas assets """
        return self.all_resources["SpriteAtlas"]

    @property
    def monoscripts(self) -> list[MonoScript]:
        """ Returns all parsed MonoScript assets """
        return self.all_resources["MonoScript"]

    @property
    def monobehaviours(self) -> list[MonoBehaviour]:
        """ Returns all parsed MonoBehaviour assets """
        return self.all_resources["MonoBehaviour"]
