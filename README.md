This python script is a unpacker/packer for assets file in Pandora's box DX game boards.
Pandora's box DX game boards is great product for arcade game player. It preinstalled 3000 games.
And it run a retroarch and several game cores to emulate all 3000 games, and its assets is encrypted. 
Users can not mod UI, logo files are stored in NAND IC onboard, so it's hard to change logo files.
There are 3 files with .zip extension in the roms folder of TF card,  they are had.zip hadc.zip and rade.zip.
These files are not game roms, they are actually packaged asset files.
You can use this script to unpack/pack these 3 files 

Usage: 
   * unpack 
```
    ./filepack.py -e <source file> <target folder>     
    # this command will copy source to target folder 
    # ./filepack.py -e hadc.zip /tmp/dumped
```
    
*   pack 
```
    ./filepack.py -p <source file> <target file>   
    # source file actually is the copyed file , scipt will find unpacked files base the source file location
    #./filepack.py -p /tmp/dumped/hadc.zip /tmp/hadc.zip
```

note:
    1. Asset package file only store crc32 code of every file, and the file name information is lost, so I use file names, this file lists all filename I known.
    2. Main program extrace asset package file into /tmp/, if there is file nameed retroarch in /tmp/, main program will run /tmp/retroarch instead of retroarch in NAND when users start a game, ( not all games are run with retroarch, but the first game KOF97 is ), so you can add your own retroarch into asset package file.  but i found this method is not alwayws work , maybe stock firmware updated. 
    3. You'd better use Python3


References:
    1. [link for blog on Pandora's box DX game boards  ]( https://zerojay.com/blog/pandoraboxdx) 
    2. [link for Pandora's box DX game board on Aliexpress   ]( https://www.aliexpress.com/i/4000906970186.html)
