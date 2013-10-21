#############################
#    SZ, TZ, ZM             #
#    10/3/2013              #
#    assembler.py           #
#############################

from assembly_parser import assembly_parser
from instruction_table import instruction_table
from register_table import register_table
from pseudoinstruction_table import pseudoinstruction_table

import sys
import getopt

def usage():
    print 'Usage: '+sys.argv[0]+' -i <file1>'
    sys.exit(1)

def main(argv):
    files = argv
    if len(files) is not 1:
        usage()
    for filename in files:
        asm           = open(filename)
        lines         = asm.readlines()
        parser        = assembly_parser(64, instruction_table, register_table, pseudoinstruction_table,4)
        parser.first_pass(lines)
        parser.second_pass(lines)


if __name__ == '__main__':
    main(sys.argv[1:])

