import svgwrite

dwg = svgwrite.Drawing('test.svg', profile='full')
dwg.add(dwg.line((0, 0), (16, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 16), font_size='5px', fill='red'))



def connect_points(a, b, d):
    d.add(d.circle(center=a, r=40))
    d.add(d.circle(center=b, r=40))
    d.add(d.line(a, ((a[0] + b[0]) / 2, a[1]), stroke=svgwrite.rgb(10, 10, 16, '%')))
    d.add(d.line(((a[0] + b[0]) / 2, a[1]), ((a[0] + b[0]) / 2, b[1]), stroke=svgwrite.rgb(10, 10, 16, '%')))
    d.add(d.line(((a[0] + b[0]) / 2, b[1]), b, stroke=svgwrite.rgb(10, 10, 16, '%')))


connect_points((128,128), (512, 512), dwg)

dwg.save()