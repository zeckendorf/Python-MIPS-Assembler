#############################
#    SZ, TZ, ZM             #
#    10/3/2013              #
#    assembler.py           #
#############################

from assembly_parser import assembly_parser
import sys
from instruction_table import instruction_table
from register_table import register_table
from pseudoinstruction_table import pseudoinstruction_table


files = sys.argv[1:]
for filename in files:
    asm           = open(filename)
    lines         = asm.readlines()
    parser        = assembly_parser(64, instruction_table, register_table, pseudoinstruction_table)
    parser.first_pass(lines)
    parser.second_pass(lines)

#commands = parser.make_commands(lines,symbol_table) # turn lines into command objects using parser2's parse function

#hack_file = open(asm_file_name + '.hack', 'w') # Open the .hack file for writing
#parser2.write_commands(commands, hack_file, symbol_table, var_sym_start) # Send list of commands to parser to write to .hack file
#hack_file.close() # Close the .hack file.