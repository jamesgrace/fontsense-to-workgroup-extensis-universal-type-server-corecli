# fontsense-to-workgroup-extensis-universal-type-server-corecli

usage: `fontsense_to_workgroup.py [-h] [-o OUTPUT] -i INPUT -w WORKGROUP`

References a text file containing a listing of FontSense checksums and then
adds corresponding fonts to a designated Universal Type Seerver Workgroup.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output folder location ( enquoted + case sensitive
                        absolute path with trailing slash ).

required arguments:
  -i INPUT, --input INPUT
                        Input file ( enquoted + case sensitive ) containing
                        list of FontSense IDs.
  -w WORKGROUP, --workgroup WORKGROUP
                        Workgroup ( enquoted + case-sensitive ) within UTS
                        that fonts will be added to.
