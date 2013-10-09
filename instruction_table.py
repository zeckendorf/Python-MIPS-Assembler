#############################
#    SZ, TZ, ZM             #
#    10/3/2013              #
#    instruction_table.py   #
#############################

# Create the Symbol Table as a dictionary. This table stores ROM addresses of each reserved register in our MIPS
# Assembler


# nstruction format length
# 6 : R
# 4 : I
# 2 : J

# All values in HEX
instruction_table = {
	'add'   : ['0x00','rs','rt','rd','shamt','0x20'],
	'addi'  : ['0x08','rs','rt','imm'],
	'addiu' : ['0x09','rs','rt','imm'],
	'addu'  : ['0x00','rs','rt','rd','shamt','0x21'],
	'and'   : ['0x00','rs','rt','rd','shamt','0x24'],
	'andi'  : ['0x0C','rs','rt','imm'],
	'beq'   : ['0x04','rs','rt','imm'],
	'bne'   : ['0x05','rs','rt','imm'],
	'j'     : ['0x02', 'add'],
	'jal'   : ['0x03', 'add'],
	'jr'    : ['0x00','rs','rt','rd','shamt','0x08'],
	'lbu'   : ['0x24','rs','rt','imm'],
	'lhu'   : ['0x25','rs','rt','imm'],
	'll'    : ['0x30','rs','rt','imm'],
	'lui'   : ['0x0F','rs','rt','imm'],
	'lw'    : ['0x23','rs','rt','imm'],
	'nor'   : ['0x00','rs','rt','rd','shamt','0x27'],
	'or'    : ['0x00','rs','rt','rd','shamt','0x25'],
	'ori'   : ['0x0D','rs','rt','imm'],
	'slt'   : ['0x00','rs','rt','rd','shamt','0x2A'],
	'slti'  : ['0x0A','rs','rt','imm'],
    'sltiu' : ['0x0B','rs','rt','imm'],
	'sltu'  : ['0x00','rs','rt','rd','shamt','0x2B'],
	'sb'    : ['0x28','rs','rt','imm'],
	'sc'    : ['0x38','rs','rt','imm'],
	'sh'    : ['0x29','rs','rt','imm'],
    'sw'    : ['0x2B','rs','rt','imm'],
	'sub'   : ['0x00','rs','rt','rd','shamt','0x22'],
	'subu'  : ['0x00','rs','rt','rd','shamt','0x23'],

    # Arithmetic Core
    'div'   : ['0x00','rs','rt','rd','shamt','0x1A'],
	'divu'  : ['0x00','rs','rt','rd','shamt','0x1B'],
    'mfhi'  : ['0x00','rs','rt','rd','shamt','0x10'],
	'mflo'  : ['0x00','rs','rt','rd','shamt','0x12']
	}