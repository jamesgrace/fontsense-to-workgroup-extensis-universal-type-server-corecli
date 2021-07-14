# fontsense-to-workgroup-extensis-universal-type-server-corecli
References a text file containing a listing of FontSense checksums and then adds corresponding fonts to a designated Universal Type Seerver Workgroup.

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
Workgroup ( _enquoted + case-sensitive_ ) within UTS that fonts will be added to.
