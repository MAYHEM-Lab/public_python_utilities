# gdcp.py

gdcp.py in this repo is an extension of [gdcp](https://github.com/ctberthiaume/gdcp.git) and a python interface to the Google Drive command line interface (CLI).  The extensions include support for delete and copy operations. The original version can be found at the github repo above or in this repo as file gdcp_orig.

See [Readme_gdcp.md]() for installation instructions and setup, as it is the same as for gdcp.

# usage (testing)

python test_gdcp.py

# usage 

usage: gdcp.py [-h] {version,list,delete,download,upload,transfer} ...

python gdcp.py version
gdcp version 0.7.13

gdcp list -i https://drive.google.com/drive/u/0/folders/XXXXXXX

