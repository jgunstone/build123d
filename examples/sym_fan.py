from build123d import *
from ocp_vscode import *
# import numpy as np
from math import pi, cos, sin, sqrt, asin
import pathlib

get_deg = lambda theta: (180/pi) * theta
radius, length, pad = 1, 5, 1

line_weight = pad / 10
cnr = (radius+ length + pad, radius + pad)  

theta = asin(radius/length)

c = sqrt(length**2-radius**2)
t1 = (c*cos(theta), c*sin(theta))
t2 = (t1[0], -1 * t1[1]) 
l1 = Line((0, 0), t1)
l2 = mirror(l1)
arc = TangentArc(t1, t2, tangent=l1 % 1)
arc1 = Rot(Z=90) * arc

lines = [l1, l2, arc]
cnrs = [cnr, (cnr[0], -cnr[1]), (-cnr[0], -cnr[1]), (-cnr[0], cnr[1]), cnr]
b_lines = [Line(cnrs[n], cnrs[n+1]) for n in range(0, len(cnrs)-1) ]

# have to rotate base objects before combing into sketch
lines = [Rot(Z=90) * l for l in lines]
b_lines = [Rot(Z=90) * l for l in b_lines]

wing1 = make_face(lines)
wing2 =  mirror(wing1, about=Plane.XZ)   # Plane.YZ if not rotated
wings = Sketch() + wing1 + wing2


exporter = ExportSVG(unit=Unit.MM, line_weight=0)
exporter.add_layer("wings", fill_color=(0, 0, 0))
exporter.add_shape(wings, layer="wings")
exporter.add_layer("border", line_weight=line_weight)
[exporter.add_shape(b, layer="border") for b in b_lines]
fname = pathlib.Path(__file__).stem
exporter.write(f"{fname}.svg")