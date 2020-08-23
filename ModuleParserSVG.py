import re
import Module
import ModToSVG
vtext = open("basic.laz")
line = vtext.readline()
mod = Module.Module()
dwg = svgwrite.Drawing('basic.svg', profile='full')
in_x = 100
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
                dwg.add()-------------------------------------------------------------------------------------------------------------
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
ModToSVG.draw(mod)
