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

Extended operations:   

* Move file 1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A to folder 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl:     
```
python gdcp.py move -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A -p 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl
```

* Move file 1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A to the root folder:      
```
python gdcp.py move -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A
```

* Link file 1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A in folder 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl without removing it from its current folder (create an alias).  Note that if you delete this file, it will be removed from all folders it is linked to.     
```
python gdcp.py move -k -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A
```

* BE CAREFUL WITH THIS ONE -- when its gone its gone!! If the file is in multiple folders, it will be deleted from all.  
Delete file 1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A:    
```
python gdcp.py delete -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A
```
