"""
CadQuery script for creating an own base symbol for a fan.

WORK IN PROGRESS.
"""

import cadquery as cq
import math


# PARAMETERS

# Options for object showing, solid grey with no transparency
options = {'rgba': (204, 204, 204, 0.0)}

b_body_diam = 75.0  # Diameter of whole base
b_body_inner_thickness = 2.0  # Thickness of inner parts of base

b_body_outer_thickness = 3.0  # Thickness of outer parts of base
b_body_outer_ring_width = 2.0  # Width of outer base ring

p_post_outer_diameter = 4.0   # Inner diameter of the screwposts
p_post_inner_diameter = 2.0   # Outer diameter of the screwposts
p_post_height = 6.0   # Height of the screwpoints

triangle_side_len = 45.0   # Diameter of enclosing traingle circle (mm)


# LOGIC


def calc_triangle_polygon_diam(side_len):
    """
    Function for calculating diameter of enclosing triangle circle.

    Apparently the polygon function creates a circle of certain diameter and
    then creates a polygon inside, so we have to calculate the triangle
    axes lengths ourselves.

    :param side_len: length of triangle side
    """
    const_angle = math.radians(30)
    return side_len / math.cos(const_angle)


def calc_inner_ring_radius(body_diam, outer_ring_width):
    """
    Function for calculating the radius of the inner ring.

    The base will have a small portruded ring around it, just like the
    original, so we have to make the inner circle a bit smaller, accounting
    for the out ring.

    :param body_diam: diameter of whole base panel
    :param outer_ring_width: width of the outer ring
    """
    ret_body_diam = body_diam - (outer_ring_width * 2.0)
    return ret_body_diam / 2.0


inner_ring_radius = calc_inner_ring_radius(b_body_diam,
                                           b_body_outer_ring_width)
box = cq.Workplane('front') \
        .circle(inner_ring_radius) \
        .extrude(b_body_inner_thickness)

# Create triangle for vertices
polygon_circle_diam = calc_triangle_polygon_diam(triangle_side_len)
triangle = box.faces('>Z') \
        .workplane(-b_body_inner_thickness) \
        .polygon(3, polygon_circle_diam, forConstruction=True) \
        .vertices()

for v in triangle.all():
    v.circle(p_post_outer_diameter / 2.0) \
     .circle(p_post_inner_diameter / 2.0) \
     .extrude(-p_post_height, True)

# Create outer ring for base
outer_ring = box.faces('>Z') \
        .workplane() \
        .circle(inner_ring_radius) \
        .circle(b_body_diam / 2.0) \
        .extrude(b_body_outer_thickness)

result = outer_ring

# Display results
show_object(result, options=options)  # noqa
