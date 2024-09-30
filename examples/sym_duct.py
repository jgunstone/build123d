from typing import Tuple, Union, Literal
from build123d import *
from ocp_vscode import *
import numpy as np
from math import pi, cos


area = 


width = 20
height = 5




rec = Rectangle(width=width, height=height)
ci = Circle(radius=r)
show_object([tri, ci])

exporter = ExportSVG(unit=Unit.MM, line_weight=0)



exporter.add_layer("ci", fill_color=(255, 255, 255), line_weight=x/20)  # , line_weight=1
exporter.add_shape(ci, layer="ci")

exporter.add_layer("tri", fill_color=(0, 0, 0), line_weight=0)
exporter.add_shape(tri, layer="tri")



fname = pathlib.Path(__file__).stem
exporter.write(f"{fname}.svg")