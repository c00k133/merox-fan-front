import cadquery as cq
import math


class FanBase:

    def __init__(self,
                 body_diam=75.0,
                 body_inner_thickness=2.0,
                 body_outer_thickness=1.0,
                 body_outer_ring_width=2.0,
                 post_outer_diameter=4.0,
                 post_inner_diameter=2.0,
                 post_height=4.0,
                 triangle_side_len=45.0,
                 options={'rgba': (204, 204, 204, 0.0)}):
        """
        Initialize new FanBase object.

        :param options: options for CadQuery's `show_object` function,
                        defaults to grey with zero transparency
        """
        self.body_diam = body_diam
        self.body_inner_thickness = body_inner_thickness
        self.body_outer_thickness = body_outer_thickness
        self.body_outer_ring_width = body_outer_ring_width
        self.post_outer_diameter = post_outer_diameter
        self.post_inner_diameter = post_inner_diameter
        self.post_height = post_height
        self.triangle_side_len = triangle_side_len
        self.options = options

    def _calc_triangle_polygon_diam(self):
        """
        Method for calculating diameter of enclosing triangle circle.

        Apparently the polygon function creates a circle of certain diameter
        and then creates a polygon inside, so we have to calculate the triangle
        axes lengths ourselves.
        """
        const_angle = math.radians(30)
        return self.triangle_side_len / math.cos(const_angle)

    def _calc_inner_ring_radius(self):
        """
        Method for calculating the radius of the inner ring.

        The base will have a small portruded ring around it, just like the
        original, so we have to make the inner circle a bit smaller, accounting
        for the out ring.
        """
        ret_body_diam = self.body_diam - (self.body_outer_ring_width * 2.0)
        return ret_body_diam / 2.0

    def _create_screw_posts(self, triangle_vertices):
        for v in triangle_vertices.all():
            v.circle(self.post_outer_diameter / 2.0) \
             .circle(self.post_inner_diameter / 2.0) \
             .extrude(-self.post_height, True)

    def _calc_outer_ring_thickness(self):
        """
        Helper function for calculating outer ring thickness.
        Used for confining to PEP8 line length.
        """
        return self.body_outer_thickness + self.body_inner_thickness

    def create(self):
        """
        Create a CadQuery object out of this FanBase object.
        """
        inner_ring_radius = self._calc_inner_ring_radius()
        box = cq.Workplane('front') \
                .circle(inner_ring_radius) \
                .extrude(self.body_inner_thickness)

        # Create triangle for vertices
        polygon_circle_diam = self._calc_triangle_polygon_diam()
        triangle = box.faces('>Z') \
                      .workplane(-self.body_inner_thickness) \
                      .polygon(3, polygon_circle_diam, forConstruction=True) \
                      .vertices()
        self._create_screw_posts(triangle)

        # Create outer ring for base
        outer_ring_thickness = self._calc_outer_ring_thickness()
        outer_ring = box.faces('>Z') \
                        .workplane() \
                        .circle(self.body_diam / 2.0) \
                        .circle(inner_ring_radius) \
                        .extrude(-outer_ring_thickness)

        return outer_ring

    def show(self, options=None):
        """
        Run this base through CadQuery's `show_object` function.

        :param options: optional options parameter for `show_object`, defaults
                        to options initialized with this object
        """
        if options is None:
            options = self.options
        show_object(self.create(), options=options)  # noqa  # ignore PEP8


#FanBase().show()
fanbase = FanBase().create()

fanbase.faces('<Z') \
       .circle(fanbase.inner_ring_radius) \

