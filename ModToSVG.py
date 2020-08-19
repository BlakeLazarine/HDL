import Module
import svgwrite
def draw(mod):
    gap = 200
    dwg = svgwrite.Drawing('test.svg', profile='full')
    for i in range(len(mod.inputs)):
        dwg.add(dwg.circle(center=(100, 100 + 100*i), r=40))