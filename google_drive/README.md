# gdcp.py

gdcp.py in this repo is an extension of [gdcp](https://github.com/ctberthiaume/gdcp.git) and a python interface to the Google Drive command line interface (CLI).  The extensions include support for delete and copy operations. The original version can be found at the github repo above or in this repo as file gdcp_orig.
Both use [v2](https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/drive_v2.files.html) of the Google Drive [API](https://developers.google.com/drive/api/v2/about-sdk).

See the [Readme](https://github.com/ctberthiaume/gdcp.git) for gdcp.md for the installation instructions and setup, as it is the same as for gdcp.

You get the file URLs by going to Google Drive, opening the file and cutting/pasting the URL.  To get the folder ID, go to Google Drive, navigate to the folder and when in it, view the URL and cut/past the final long string that follows the last forward slash in the URL.  Your root folder does not have such a folder ID exposed in the URL -- if you want to move/copy a file to the root folder, just leave off the folder ID and the tool will find the root folder for you.

# usage (testing)

python test_gdcp.py

# usage 

usage: gdcp.py [-h] {version,list,delete,download,upload,transfer} ...

python gdcp.py version  
gdcp version 0.8.1

gdcp list -i https://drive.google.com/drive/u/0/folders/XXXXXXX

Extended operations:   

* Copy the file at URL https://docs.google.com/document/d/1DSEWBvjWqUtvENXWO-kdQGjkezzY4CrO5Wh8cmBxliM (-i argument) to new file named newname (-n argument) and place it in the folder identified by ID 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl
```
python gdcp.py copy -i https://docs.google.com/document/d/1DSEWBvjWqUtvENXWO-kdQGjkezzY4CrO5Wh8cmBxliM -n "newname" -p 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl
```

* Move file https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A to folder with ID 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl     
```
python gdcp.py move -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A -p 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl
```

* Move file https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A to the root folder      
```
python gdcp.py move -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A
```

* Link the file https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A into the folder with ID 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl without removing it from its current folder (i.e. create an alias).  Note that if you delete this file, it will be removed from all folders it is linked to and located in.  The only difference here is the use of the -k option.  You can leave off the -p option if you want to link the file in your root folder.
```
python gdcp.py move -k -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A -p 1kurav0jGmZfP3ZLhs2niVXfAj2tYYoLl
```

* BE CAREFUL WITH THIS ONE -- when its gone its gone!! If the file is in multiple folders, it will be deleted from all.  
Delete file https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A    
```
python gdcp.py delete -i https://docs.google.com/document/d/1siMp1RA8azMb7t0UppYFjT_a9J-dy7BTjAqCCxZyS-A
```
