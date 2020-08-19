# import re
# vtext = open("ha1_1.v").read()
# operations = ['+', '-', '*', '/', '<', '>', '==', '!', '!=', '<<', '>>', '|', '&', '||', '&&', '^', '%', '<=', '>=']
# special = '?:()'
# input_names = []
# output_names = []
# for i in re.findall(r'input(.*)[;,]', vtext):
#     input_names += [s.strip().split(' ')[-1] for s in i.split(',')]
#
# for i in re.findall(r'output(.*)[;,]', vtext):
#     output_names += [s.strip().split(' ')[-1] for s in i.split(',')]
# print(input_names)
# print(output_names)
#
# for n in output_names:
#     print(n + ' = ' + re.search(n + r'.*[^!>=]=[^=](.*);', vtext).group(1))


#try 2

import re
import Module
vtext = open("basic.laz")
line = vtext.readline()
mod = Module.Module()
while line:
    # print(line)
    line = re.sub(' +', ' ', line)
    line = re.sub('\t', '', line)
    line = re.sub(r'\/\/.*', '', line)
    command = re.match(r' *(\w+)(?= )', line)

    if command:
        # print(command.group(1))
        if command.group(1) == 'input':
            full = re.match(r' *input (\w+)\[(\d+)\] *', line)
            if full:
                mod.add_input(full.group(1), int(full.group(2)))

            else:
                print('syntax error in line:', line)
        elif command.group(1) == 'output':
            full = re.match(r' *output (\w+)\[(\d+)\] *', line)
            if full:
                mod.add_output(full.group(1), int(full.group(2)))
            else:
                print('syntax error in line:', line)
        elif command.group(1) == 'wire':
            full = re.match(r' *wire (\w+)\[(\d+)\] *= *(.+)', line)
            if full:
                mod.add_wire(full.group(1), int(full.group(2)), full.group(3))
            else:
                print('syntax error in line:', line)
        elif command.group(1) == 'reg':
            full = re.match(r' *reg (\w+)\[(\d+)\] \((\d+), *(posedge|negedge) (\w+)\) *= *(.+)', line)
            if full:
                mod.add_reg(full.group(1), full.group(2), full.group(3), full.group(4), full.group(5), full.group(6))
            else:
                full = re.match(r' *reg (\w+)\[(\d+)\] \((\d+), *(posedge|negedge) (\w+)\) *', line)
                if full:
                    mod.add_reg(full.group(1), full.group(2), full.group(3), full.group(4), full.group(5))
                else:
                    print('syntax error in line:', line)
        elif command.group(1) == 'assign':
            full = re.match(r' *assign (\w+) *= *(.+)', line)
            if full:
                mod.assign(full.group(1), full.group(2))
            else:
                print('syntax error in line:', line)

    line = vtext.readline()


# mod.print_info()
mod.set_in('abc', 1)
mod.set_in('d', 2)
print(mod.update())
mod.set_in('up', 1)
print(mod.update())
mod.set_in('up', 0)
mod.set_in('abc', 5)
print(mod.update())
mod.set_in('up', 1)
print(mod.update())
mod.set_in('up', 0)
mod.set_in('up', 1)
print(mod.update())