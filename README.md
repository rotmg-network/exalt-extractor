# Exalt Asset Extractor

A tool designed for extracting and handling assets from Realm of the Mad God Exalt. This aims to simplify the process of gathering spritesheets, XML data files, network packet names and more. Written in Python.  
  
## Features  
- **Asset Extraction**: Easily extract various game assets including spritesheets, sounds, textures, 3D models, XML sheets, network packet names and more.  
- **Extendable**: The UnityExtractor class can easily be extended to extract any types of assets.  
- **User-Friendly**: No user input needed. The most important assets will be extracted automatically but can be customized with command line options (see below).  
- **Cross-Platform**: Compatible with Windows and MacOS.  

## Installation  
  
To get started follow these simple installation steps:  

```bash
# Clone the repository
git clone https://github.com/rotmg-network/exalt-extractor.git

# Navigate to the project directory
cd exalt-extractor

# Install dependencies
pip install -r requirements.txt
```  

## Usage  
  
To extract assets, run the following command:  
  
```bash
python extractor.py
```  
This will extract a limited amount of assets (spritesheets, XML files, packet names) to the `output` folder. You can specify single asset types, change the output folder and more with command line flags.  
  
```bash
python extractor.py [options]
# Set the output folder to "assets" and extract spritesheets only:
python extractor.py --output 'assets' --spritesheets
# Extract packet names and 3D models only:
python extractor.py --packets --models
```  
  
Replace [options] with your specific command-line options to customize the extraction process. For detailed usage instructions, refer to the help provided by the utility:

```bash
python extractor.py --help
```

## Contributing  
  
Contributions to the project are welcome! If you're interested in enhancing the functionality, fixing bugs, or improving documentation, please feel free to fork the repository and submit a pull request.  

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)  
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)  
4. Push to the Branch (`git push origin feature/AmazingFeature`)  
5. Open a Pull Request
  
## TODO  

Features and fixes in progress  

- [ ] Remove the need for the colorama library which means no need for a requirements file
- [ ] Add functionality to split up spritesheets based on the JSON file settings
- [ ] Parse and rebuild the original assets based on the assets manifest files
- [ ] Parse the current game build based on global-metadat? Or out of scope for an asset extractor