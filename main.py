import os
import time
from sys import argv, exit as exit_program
from argparse import ArgumentParser, Namespace
from utils import Logger, Resources, UnityExtractor

logger = Logger()


def main(args: Namespace):
    """ The entry point of the program """
    start_time = time.time()
    # logger.info(f"Arguments: {vars(args)}\n")

    # check for a custom output path or fallback to the default
    output_path = args.output
    assert_path_exists(output_path)
    logger.info(f"Using output folder: '{output_path}'")

    # check for a custom input path
    if args.input is not None:
        resources = Resources(args.input)
    else:
        resources = Resources()

    extractor = UnityExtractor(resources, output_path)

    extractor.extract_packets()  # extract all packet names
    extractor.extract_xml(True)  # save all XML sheet files
    extractor.extract_spritesheets(True)  # save all spritesheet .png files and spritesheet.json
    extractor.extract_manifests()  # save both the manifest_json json and xml files

    print()  # line break
    logger.success(f"Finished in {round((time.time() - start_time), 2)} seconds\n")


def assert_path_exists(path: str):
    """ Attempt to create a path if it doesn't exist and exit if it fails """
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception as e:
            logger.critical(f"Could not create path '{path}': {e}\n")
            exit_program(1)


if __name__ == '__main__':
    desc = "Extract game data from the RotMG Exalt Unity resource files."
    desc += " If no arguments are passed, it will try to extract all possible assets."
    usage = f"python3 {argv[0]} [optional arguments]"

    parser = ArgumentParser(description=desc, usage=usage)
    parser.add_argument('-o', '--output', type=str, default="output",
                        help='the output directory for extracted data (default: "output")')
    parser.add_argument('-i', '--input', type=str,
                        help='use a custom Exalt resources directory')
    # parser.add_argument('-p', '--packets', action='store_true', help='extract all packet names.')
    # parser.add_argument('-b', '--binary', type=str, help='override the local GameAssembly.dll path.')
    # parser.add_argument('-m', '--metadata', type=str, help='override the local global-metadata.dll path.')
    # parse CLI arguments and run the program
    arguments = parser.parse_args()
    main(arguments)
