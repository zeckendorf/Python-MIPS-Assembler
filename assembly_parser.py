##############################
#    SZ, TZ, ZM              #
#    10/3/2013               #
#      assembly_parser.py    #
##############################

import re

#TODO: Finish calculating instruction size
#TODO: Add pseudoinstruction handlers
#TODO: Convert hexidecimal and binary to decimal
class command(object):
    def __init__(self, cmd_string):
        return


class assembly_parser(object):

    # Default memory location
    default_mem_loc   = 0

    # List of labels and their respective locations
    symbol_table        = {}

    # Current location in memory
    current_location  = 0

    # dictionary of memory locations w/ their values
    system_memory     = {}

    # current instruction table
    instruction_table = {}

    # current symbol table
    register_table      = {}

    # current pseudoinstruction table
    pseudinstr_table  = {}

    def __init__(self, default_memory_location, instruction_table, register_table, pseudoinstruction_table):
        ''' Initialize tables and memory
        '''
        self.default_mem_loc    = default_memory_location
        self.instruction_table  = instruction_table
        self.register_table     = register_table
        self.pseudinstr_table   = pseudoinstruction_table


        return

    def first_pass(self, lines):
        ''' For first pass, calculate size in mem of each instruction for calculating addressing
        '''
        self.current_location = self.default_mem_loc
        for line in lines:

            # Sanitize string
            if '#' in line:
                line = line[0:line.find('#')]

            # Sanitize string
            line = line.strip()
            if not len(line):
                continue

            # Make sure memory location lines up with divisions of 4
            if self.current_location % 4 is not 0:
                self.current_location += 4 - self.current_location % 4

            # Label recognition
            if ':' in line:
                label = line[0:line.find(':')]
                self.symbol_table[label] = str(self.current_location)
                line = line[line.find(':') + 1:].strip()

            # Go to proper address, increment for all stored memory
            if '.' in line:
                if '.org' in line:
                    self.current_location = int(line[line.find('.org') + len('.org'):])
                    continue
                if '.byte':
                    bytes = line[line.find('.byte') + len('.byte'):].split(',')
                    for byte in bytes:
                        self.current_location += 1
                    continue

            # Make sure memory location lines up with divisions of 4
            if self.current_location % 4 is not 0:
                self.current_location += 4 - self.current_location % 4


            # Parse instructions to establish mem size
            instruction = line[0:line.find(' ')]
            args        = line[line.find(' ') + 1:].replace(' ', '').split(',')

            # Sanitize arguments so every numeric is decimal
            acount = 0
            for arg in args:
                if arg not in self.symbol_table.keys():
                    if arg[-1] == 'H':
                        args[acount] = str(int(arg[:-1], 16))
                    elif arg[-1] == 'B':
                        args[acount] = str(int(arg[:-1], 2))
                acount += 1

            self.current_location += self.calculate_instruction_size(instruction, args)

    def second_pass(self, lines):
        ''' For second pass, we convert assembly to machine code
        '''

        self.current_location = self.default_mem_loc
        for line in lines:

            # Sanitize string
            if '#' in line:
                line = line[0:line.find('#')]
            line = line.strip()
            if not len(line):
                continue

            # Make sure memory location lines up with divisions of 4
            if self.current_location % 4 is not 0:
                self.current_location += 4 - self.current_location % 4

            # Label ignorator
            if ':' in line:
                line = line[line.find(':') + 1:].strip()

            # Assembler directives: .org, .byte, etc.
            if '.' in line:
                if '.org' in line:
                    self.current_location = int(line[line.find('.org') + len('.org'):])
                    continue
                if '.byte':
                    bytes = line[line.find('.byte') + len('.byte'):].split(',')
                    for byte in bytes:
                        byte = byte.strip()
                        if 'H' in byte:
                            byte = hex(int(byte[0:-1], 16))
                        elif 'B' in byte:
                            byte = hex(int(byte[0:-1], 2))
                        else:
                            byte = hex(int(byte))

                        self.store_bit_string(self.hex2bin(byte.strip(), 8))
                    continue

            # Make sure memory location lines up with divisions of 4
            if self.current_location % 4 is not 0:
                self.current_location += 4 - self.current_location % 4

            # Parse the line!
            instruction = line[0:line.find(' ')]
            args        = line[line.find(' ') + 1:].replace(' ', '').split(',')

            # Sanitize arguments so every numeric is decimal
            acount      = 0
            for arg in args:
                if arg not in self.symbol_table.keys():
                    if arg[-1] == 'H':
                        args[acount] = str(int(arg[:-1], 16))
                    elif arg[-1] == 'B':
                        args[acount] = str(int(arg[:-1], 2))
                acount += 1



            # Create function code from instruction table
            # if instruction in self.pseudinstr_table.keys():
            #  self.parse_pseudoinstruction(instruction, args)
            if instruction in self.instruction_table.keys():
                self.parse_instruction(instruction, args)
            else:
                print "INSTRUCTION: " + instruction + " IS INVALID! ABORT"
                exit()

        self.print_memory_map()

    def parse_instruction(self, instruction, args):
        ''' Parses instruction, places proper hex into memory
            Different cases for R, I, J instructions
        '''

        machine_code = self.instruction_table[instruction]

        # parse arguments
        arg_count = 0
        offset    = 0
        for arg in args:
            if '(' in arg:

                # Parse offset from known syntax
                offset   = hex(int(arg[0:arg.find('(')]))
                register = re.search('\((.*)\)', arg)

                # Location in memory is offset from memory location
                location = self.register_table[register.group(1)]
                register = hex(location)

                # Finish processing args
                args[arg_count] = register

            elif arg in self.register_table.keys():

                # Replace symbol with value in table
                args[arg_count] = hex(int(self.register_table[arg]))

            elif arg in self.symbol_table:
                # Replace label with its value
                args[arg_count] = self.symbol_table[arg]

            # Increment argument counter for modifying list
            arg_count += 1


        # R instruction
        if len(machine_code) == 6:

            # Set rs, rt, rd, and offset in the machine_code
            rs = args[1]
            rt = args[2]
            rd = args[0]
            machine_code[1] = rs
            machine_code[2] = rt
            machine_code[3] = rd
            machine_code[4] = '0'

            # Get binary of machine code
            op_binary = self.hex2bin(machine_code[0], 6)
            rs_binary = self.hex2bin(machine_code[1], 5)
            rt_binary = self.hex2bin(machine_code[2], 5)
            rd_binary = self.hex2bin(machine_code[3], 5)
            shamt_bin = self.hex2bin(machine_code[4], 5)
            funct_bin = self.hex2bin(machine_code[5], 6)

            # Create 32-bit string to divide up into bytes
            bit_string = op_binary + rs_binary + rt_binary + rd_binary + shamt_bin + funct_bin
            self.store_bit_string(bit_string)

            return

        # I instruction
        if len(machine_code) == 4:

            # Set rs, rt, imm in the machine_code
            rs  = args[1]
            rt  = args[0]
            imm = offset
            if len(args) == 3:
                imm = hex(int(args[2]))

            machine_code[1] = rs
            machine_code[2] = rt
            machine_code[3] = imm

            # Get binary of machine code
            op_binary = self.hex2bin(machine_code[0], 6)
            rs_binary = self.hex2bin(machine_code[1], 5)
            rt_binary = self.hex2bin(machine_code[2], 5)
            im_binary = self.hex2bin(machine_code[3], 16)

            # Create 32-bit string to divide up into bytes
            bit_string = op_binary + rs_binary + rt_binary + im_binary
            self.store_bit_string(bit_string)

            return

        # J instruction
        if len(machine_code) == 2:

            # Create hex machine code
            address = args[0]
            machine_code[1] = hex(int(address))

            # Create binary bit string
            op_binary      = self.hex2bin(machine_code[0], 6)
            address_binary = self.hex2bin(machine_code[1], 26)
            bit_string = op_binary + address_binary

            # Store bit string in memory
            self.store_bit_string(bit_string)

            return

        return

    def parse_pseudoinstruction(self, instruction, args):
        return

    def calculate_instruction_size(self, instruction, args):
            ''' Calculate instruction size for first pass in bytes
            '''

            if instruction in self.pseudinstr_table:

                # Check for overloaded instruction: beq
                if instruction == 'beq':
                    if not '$' in args[1]:
                        if self.value_outside_range(int(args[1])):
                            return 12
                        else:
                            return 8
                    else:
                        return 4

                #li check for size of argument
                if instruction == 'li':
                    if self.value_outside_range(int(args[1])):
                        return 8
                    else:
                        return 4

                #addi check for size of argument
                if instruction == 'addi':
                    if self.value_outside_range(int(args[2])):
                        return 8
                    else:
                        return 4

                #lw check for size of argument
                if instruction == 'lw':
                    if '(' in args[1]:
                        # Parse offset from known syntax
                        offset = int(args[1][0:args[1].find('(')])
                        if self.value_outside_range(offset):
                            return 8
                        else:
                            return 4

                if instruction == 'bge':
                    return 8
                if instruction == 'bgt' or instruction == 'ble':
                    return 12

                # move and clear always are 4 bytes
                return 4

            if instruction in self.instruction_table:
                return 4

    def hex2bin(self, hex_val, num_bits):
        ''' Returns binary string of num_bits length of hex value (pos or neg)
        '''

        # Adjust for negative
        tc = False
        if '-' in hex_val:
            tc = True
            hex_val = hex_val.replace('-', '')

        bit_string = '0' * num_bits
        bin_val    = str(bin(int(hex_val, 16)))[2:]
        bit_string = bit_string[0: num_bits - len(bin_val)] + bin_val + bit_string[num_bits:]

        # 2's complement if negative hex value
        if tc:
            tsubstring = bit_string[0:bit_string.rfind('1')]
            rsubstring = bit_string[bit_string.rfind('1'):]
            tsubstring = tsubstring.replace('1', 'X')
            tsubstring = tsubstring.replace('0', '1')
            tsubstring = tsubstring.replace('X', '0')
            bit_string = tsubstring + rsubstring

        return bit_string

    def store_bit_string(self, bit_string):
        ''' Store bit string into current memory block
        '''
        for i in range(0, len(bit_string) - 1, 8):
            self.system_memory[self.current_location] = bit_string[i:i + 8]
            self.current_location += 1
            #self.print_memory_map()

    def print_memory_map(self):
        print "The memory map is:\n"
        keylist = self.system_memory.keys()
        keylist.sort()
        for key in keylist:
            print "%s: %s" % (key, self.system_memory[key])

        print "\nThe label list is: " + str(self.symbol_table)
        print "\nThe current location is: " + str(self.current_location)

    def value_outside_range(self, value):
        return value > (pow(2, 15) - 1) or value < -(pow(2, 15))