import Module
import svgwrite
import re

def connect_points(a, b, d, idx=0, tot=1):
    # d.add(d.polyline([a, ((a[0] + b[0]) / 2, a[1]), ((a[0] + b[0]) / 2, b[1]), b], stroke=svgwrite.rgb(0, 0, 0, '%')))
    mid_x = (b[0] - a[0]) * ((idx + 1) / (tot + 1)) + a[0]
    # mid_x = (a[0] + b[0]) * ((idx + 1) / (tot + 1))
    d.add(d.line(a, (mid_x, a[1]), stroke=svgwrite.rgb(0, 0, 0, '%')))
    d.add(d.line((mid_x, a[1]), (mid_x, b[1]), stroke=svgwrite.rgb(0, 0, 0, '%')))
    d.add(d.line((mid_x, b[1]), b, stroke=svgwrite.rgb(10, 10, 16, '%')))


def draw(mod):
    gap = 200
    l = 80

    dwg = svgwrite.Drawing('mod.svg', profile='full')
    in_locs = []
    for i in range(len(mod.inputs)):
        dwg.add(dwg.circle(center=(100, 100 + 100*i), r=40))
        in_locs.append((100, 100 + 100*i))
        dwg.add(dwg.text(mod.inputs[i], insert=(100, 100 + 100*i), font_size='30px', fill='red'))


    wire_locs = [None for i in range(len(mod.wires))]
    furthest_x = 100
    while None in wire_locs:
        for i in range(len(mod.wires)):
            if not wire_locs[i] is None:
                continue
            wire_match = re.findall(r'wire_vals\[(\d+)\]', mod.wire_eqns[i])
            min_x = 100 + gap
            for m in wire_match:
                if wire_locs[m] is None:
                    break
                if min_x <= wirelocs[m][0]:
                    min_x = wirelocs[m][0] + gap
            else:
                y = 100
                furthest_x = max(furthest_x, min_x)
                while (min_x, y) in wire_locs:
                    y += gap
                wire_locs[i] = (min_x + l/2, y)
                #dwg.add(dwg.circle(center=(min_x, y), r=40))

                dwg.add(dwg.rect(insert = (min_x - l/2, y - l/2), size=(l,l), fill= 'white', stroke='black', stroke_width=3))
                dwg.add(dwg.text(mod.wires[i], insert=(min_x, y), font_size='30px', fill='red'))

                in_match = re.findall(r'in_vals\[(\d+)\]', mod.wire_eqns[i])
                num = len(wire_match) + len(in_match)
                for m in range(len(wire_match)):
                    connect_points(wire_locs[int(wire_match[m])], (min_x - l/2, y - l/2 + (m+1) * l / (num + 1)), dwg, m, num)
                for m in range(len(in_match)):
                    connect_points(in_locs[int(in_match[m])], (min_x - l/2, y - l/2 + (m + 1 + len(wire_match)) * l / (num + 1)), dwg, m + len(wire_match), num)
    for i in range(len(mod.outputs)):
        dwg.add(dwg.circle(center=(furthest_x + gap, 100 + 100*i), r=40))
        dwg.add(dwg.text(mod.outputs[i], insert=(furthest_x + gap, 100 + 100*i), font_size='30px', fill='red'))
        wire_match = re.findall(r'wire_vals\[(\d+)\]', mod.out_eqns[i])
        for m in wire_match:
            connect_points(wire_locs[int(m)], (furthest_x + gap, 100 + 100*i), dwg)
        in_match = re.findall(r'in_vals\[(\d+)\]', mod.out_eqns[i])
        for m in in_match:
            connect_points(in_locs[int(m)], (furthest_x + gap, 100 + 100*i), dwg)
    dwg.save()
