import re
import Module
import svgwrite
vtext = open("basic.laz")
line = vtext.readline()
mod = Module.Module()
dwg = svgwrite.Drawing('basic.svg', profile='full')
scale = 100
l = 80
in_x = scale
in_locs = []
wire_locs = []
reg_locs = []
out_locs = 1
furthest_x = scale
colors = ['black', 'blue', 'red', 'green', 'purple']
color_idx = 0

def connect_points(a, b, d, idx=0, tot=1):
    global color_idx
    global scale
    global l
    # d.add(d.polyline([a, ((a[0] + b[0]) / 2, a[1]), ((a[0] + b[0]) / 2, b[1]), b], stroke=svgwrite.rgb(0, 0, 0, '%')))
    placement = ((idx + 1) / (tot + 1) - 1)
    mid_x = (2* scale - l) * placement + b[0]

    if scale / 2 < (a[1]%(2*scale)) < scale * 3 / 2 and abs(a[1] - b[1]) > scale and b[0] - a[0] > 2 * scale:
        new_a = (a[0], a[1] - l * 3/4)
        d.add(d.line(a, new_a, stroke=colors[color_idx]))
        a = new_a

    #if a[0] % (2*scale) > scale:

    # mid_x = (a[0] + b[0]) * ((idx + 1) / (tot + 1))
    d.add(d.line(a, (mid_x, a[1]), stroke=colors[color_idx]))
    d.add(d.line((mid_x, a[1]), (mid_x, b[1]), stroke=colors[color_idx]))
    d.add(d.line((mid_x, b[1]), b, stroke=colors[color_idx]))



while line:
    # print(line)
    line = re.sub(' +', ' ', line)
    line = re.sub('\t', '', line)
    line = re.sub(r'\/\/.*', '', line)
    command = re.match(r' *(\w+)(?= )', line)

    if command:
        if command.group(1) == 'input':
            full = re.match(r' *input (\w+)\[(\d+)\] *', line)
            if full:
                mod.add_input(full.group(1), int(full.group(2)))
                dwg.add(dwg.circle(center=(scale, scale*(1+len(in_locs))), r=l/2))
                dwg.add(dwg.text(full.group(1), insert=(scale, scale*(1+len(in_locs))), font_size='30px', fill='red'))
                in_locs.append((scale, scale*(1+len(in_locs))))
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
                min_x = scale * 3
                mod.add_wire(full.group(1), int(full.group(2)), full.group(3))
                wire_match = re.findall(r'wire_vals\[(\d+)\]', mod.wire_eqns[-1])
                for m in wire_match:
                    if min_x <= wirelocs[m][0]:
                        min_x = wirelocs[m][0] + scale * 2
                y = scale
                furthest_x = max(furthest_x, min_x)
                while (min_x, y) in wire_locs:
                    y += 2 * scale
                wire_locs.append((min_x, y))
                dwg.add(dwg.rect(insert = (min_x - l/2, y - l/2), size=(l,l), fill= 'white', stroke='black', stroke_width=3))
                dwg.add(dwg.text(full.group(1), insert=(min_x, y), font_size='30px', fill='red'))

                in_match = re.findall(r'in_vals\[(\d+)\]', mod.wire_eqns[-1])
                num = len(wire_match) + len(in_match)
                for m in range(len(wire_match)):
                    loc = wire_locs[int(wire_match[m])]
                    connect_points((loc[0] + l/2, loc[1]), (min_x - l/2, y - l/2 + (m+1) * l / (num + 1)), dwg, m, num)
                for m in range(len(in_match)):
                    loc = in_locs[int(in_match[m])]
                    connect_points((loc[0] + l/2, loc[1]), (min_x - l/2, y - l/2 + (m + 1 + len(wire_match)) * l / (num + 1)), dwg, m + len(wire_match), num)
                color_idx += 1
            else:
                print('syntax error in line:', line)


        elif command.group(1) == 'reg':
            full = re.match(r' *reg (\w+)\[(\d+)\] \((\d+), *(posedge|negedge) (\w+)\) *= *(.+)', line)
            if full:
                mod.add_reg(full.group(1), full.group(2), full.group(3), full.group(4), full.group(5), full.group(6))
                wire_match = re.findall(r'wire_vals\[(\d+)\]', mod.regs[-1].eqn)
                for m in wire_match:
                    if min_x <= wirelocs[m][0]:
                        min_x = wirelocs[m][0] + scale * 2
                y = scale
                furthest_x = max(furthest_x, min_x)
                while (min_x, y) in wire_locs:
                    y += 2 * scale
                wire_locs.append((min_x, y))
                dwg.add(dwg.rect(insert = (min_x - l/2, y - l/2), size=(l,l), fill= 'white', stroke='black', stroke_width=3))
                dwg.add(dwg.text(full.group(1), insert=(min_x, y), font_size='30px', fill='red'))

                in_match = re.findall(r'in_vals\[(\d+)\]', mod.regs[-1].eqn)
                num = len(wire_match) + len(in_match)
                for m in range(len(wire_match)):
                    loc = wire_locs[int(wire_match[m])]
                    connect_points((loc[0] + l/2, loc[1]), (min_x - l/2, y - l/2 + (m+1) * l / (num + 1)), dwg, m, num)
                for m in range(len(in_match)):
                    loc = in_locs[int(in_match[m])]
                    connect_points((loc[0] + l/2, loc[1]), (min_x - l/2, y - l/2 + (m + 1 + len(wire_match)) * l / (num + 1)), dwg, m + len(wire_match), num)
                color_idx += 1

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
                if full.group(1) in mod.outputs:
                    i = mod.outputs.index(full.group(1))
                    # dwg.add(dwg.circle(center=(furthest_x + 2 * scale, scale * out_locs), r=l/2))
                    dwg.add(dwg.rect(insert = (furthest_x + 2 * scale - l/2, scale * out_locs - l/2), size=(l,l), fill= 'white', stroke='black', stroke_width=3))
                    dwg.add(dwg.text(full.group(1), insert=(furthest_x + 2* scale, scale * out_locs), font_size='30px', fill='red'))
                    wire_match = re.findall(r'wire_vals\[(\d+)\]', mod.out_eqns[i])
                    in_match = re.findall(r'in_vals\[(\d+)\]', mod.out_eqns[i])
                    num = len(wire_match) + len(in_match)

                    for m in range(len(wire_match)):
                        loc = wire_locs[int(wire_match[m])]
                        connect_points((loc[0] + l/2, loc[1]), (furthest_x + 2 * scale - l/2, scale * out_locs- l/2 + (m+1) * l / (num + 1)), dwg, m, num)

                    for m in range(len(in_match)):
                        loc = in_locs[int(in_match[m])]
                        connect_points((loc[0] + l/2, loc[1]), (furthest_x + 2 * scale - l/2, scale * out_locs - l/2 + (m + 1 + len(wire_match)) * l / (num + 1)), dwg, m + len(wire_match), num)

                    dwg.add(dwg.circle(center=(furthest_x + 4 * scale, scale * out_locs), r=l/2))
                    dwg.add(dwg.line((furthest_x + 2 * scale + l/2, scale * out_locs),(furthest_x + 4 * scale - l/2, scale * out_locs),stroke=colors[color_idx]))
                    out_locs += 1
                    color_idx += 1
            else:
                print('syntax error in line:', line)
        else:
            print('syntax error in line:', line)

    line = vtext.readline()
dwg.save()

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
