This python script is an unpacker/packer for the assets file of the Pandora's Box DX game boards.
Pandora's box DX is a great product to play arcade games. It comes with 3000 games preinstalled.

Inside, it runs retroarch and several game cores to emulate all 3000 games, and its assets are encrypted. 
Users can not modify the UI and the logo files are stored in NAND IC onboard, so it's hard to change any files.
There are 3 files with .zip extension in the roms folder of the TF card, called had.zip hadc.zip and rade.zip.

These files are not game roms, they are actually packaged asset files.
You can use this script to unpack/repack these 3 files 

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
    1. The asset package file only stores crc32 hashes of every file and the file name information is lost, so I use file the `names`. This file lists all filename I know so far.
    2. Main program extracts the asset package file into /tmp/. If there is file nameed retroarch in /tmp/, the main program will run /tmp/retroarch instead of retroarch in NAND when users start a game. (Not all games are run with retroarch, but the first game KOF97 is), so you can add your own retroarch into asset package file, but I found this method does not always work, maybe due to updated firmware. 
    3. You'd better use Python3


References:
    1. [link for blog on Pandora's box DX game boards  ]( https://zerojay.com/blog/pandoraboxdx) 
    2. [link for Pandora's box DX game board on Aliexpress   ]( https://www.aliexpress.com/i/4000906970186.html)
