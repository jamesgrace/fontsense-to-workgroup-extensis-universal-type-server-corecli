# fontsense-to-workgroup-extensis-universal-type-server-corecli
References a text file containing a listing of FontSense checksums and then adds corresponding fonts to a designated Universal Type Seerver Workgroup.

#### Requirements :
* Extensis Universal Type Server version 6.1.7 ( _or greater_ )
* Extensis Universal Type Client version 6.1.7 ( _or greater_ )
* Python 2.7.x

#### Usage :
`fontsense_to_workgroup.py [-h] [-o OUTPUT] -i INPUT -w WORKGROUP`

#### Optional Arguments :
* `-h, --help`            show this help message and exit
* `-o OUTPUT, --output OUTPUT`
Output folder location ( _enquoted + case sensitive absolute path with trailing slash_ ).

#### Required Arguments :
* `-i INPUT, --input INPUT`
Input file ( _enquoted + case sensitive_ ) containing list of FontSense IDs.
* `-w WORKGROUP, --workgroup WORKGROUP`
Workgroup ( _enquoted + case-sensitive_ ) within Universal Type Server that fonts will be added to.
