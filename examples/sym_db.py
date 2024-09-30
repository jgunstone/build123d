
from build123d import *
from ocp_vscode import *
import numpy as np

class Db(Sketch):
    def __init__(
        self, x_radius=10, y_radius=2, height=5, gap=1, scale_factor=12
    ):
        x_r, y_r, h, g = [l*scale_factor for l in [x_radius, y_radius, height, gap]]

        def get_section():
            half_arc = EllipticalCenterArc((0,0), x_radius=x_r, y_radius=y_r).mirror(Plane.XZ)
            arc = Curve() + [half_arc, half_arc.mirror(Plane.YZ)]
            return make_face(Curve() + [
                arc,
                arc.moved(Location((0, h, 0))), 
                Line(Vector(-x_r, 0), Vector(-x_r, h)),
                Line(Vector(x_r, 0), Vector(x_r, h))
            ])
            
        ell = Ellipse(x_radius=x_r, y_radius=y_r).move(Location((0, (h*3+g*3 + y_r), 0)))
        s1 = get_section().move(Location((0, (y_r), 0)))
        s2 = s1.moved(Location((0, (h+g), 0)))
        s3 = s2.moved(Location((0, (h+g), 0)))
        result = [s1, s2, s3, ell]
        super().__init__(result)
        
   

class Check(Sketch):
    def __init__(self, l1_l2_ratio: float=1/3, sf: int=50, thickness: int=5, in_circle=True):
        pt1 = np.array([0,0])
        l1, l2 = l1_l2_ratio*sf, (1-l1_l2_ratio)*sf
        pt2 = pt1 + l1*np.array([1,-1])
        pt3 = pt2 + l2*np.array([1,1])
        ln = Polyline(*[pt1, pt2, pt3])
        check = Face(ln.offset_2d(distance=thickness), color=(0,255,0))
        result = [check]
           
        super().__init__(result)
        

def export_dxf(shape, name="name"):
    exporter = ExportDXF(unit=Unit.MM, line_weight=0.5)
    exporter.add_layer("Layer 1", line_type=LineType.DASHED) # color=ColorIndex.RED, 
    exporter.add_shape(shape, layer="Layer 1")
    exporter.write(f"{name}.dxf")
    
def export_svg(shape, name="name"):
    exporter = ExportSVG(unit=Unit.MM, line_weight=0)
    exporter.add_layer("Layer 1") # , line_color=(0, 0, 255)# color=ColorIndex.RED, 
    exporter.add_shape(shape, layer="Layer 1")
    exporter.write(f"{name}.svg")


if __name__ == "__main__":

    x_radius, y_radius, height, gap, scale_factor= 10, 2, 5, 1, 1
    db = Db(x_radius=x_radius, y_radius=y_radius, height=height, gap=gap, scale_factor=scale_factor)
    
    
    scale_factor = height
    thickness = 1
    l1_l2_ratio = 1/3
    l1, l2 = l1_l2_ratio*scale_factor, (1-l1_l2_ratio)*scale_factor
    circle = Circle(scale_factor).move(Location(((l1+l2)/2, 0, 0)))
    check = Check(l1_l2_ratio=l1_l2_ratio, sf=scale_factor, thickness=thickness)
    
    mv = (7, 3, 0)
    circle.move(Location(mv))
    check.move(Location(mv))
    show_object(db)
    show_object(circle)
    show_object(check)
    
    exporter = ExportSVG(unit=Unit.MM, line_weight=0)
    
    exporter.add_layer("db", fill_color=(0, 0, 0))
    exporter.add_shape(db, layer="db")
    
    exporter.add_layer("circle", fill_color=(255, 255, 0), line_weight=0)
    exporter.add_shape(circle, layer="circle")
    
    exporter.add_layer("check", fill_color=(0, 200, 0), line_weight=0)
    exporter.add_shape(check, layer="check")
    
    fname = "db-check"
    exporter.write(f"{fname}.svg")
    

    