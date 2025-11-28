from game.helpers.BezierCurves import quadratic_bezier, generate_arc_curve
from game.particles.particle import particle

class present(particle):
    def __init__(self, x: float, y: float, scale: list, color_range: tuple, lifespan: int):

        super().__init__(x, y, scale, color_range, lifespan)
        self.start_x, self.start_y = x, y
        self.curve_points = generate_arc_curve((x, y))
        self.time = 0
        self.max_time = lifespan

        # Debug: print the curve points
        #print(f"Start: {self.curve_points[0]}")
        #print(f"Control: {self.curve_points[1]}")
        #print(f"End: {self.curve_points[2]}")


    def update(self):
        self.time += 1
        t = min(self.time / self.max_time, 1.0)

        old_x, old_y = self.x, self.y
        self.x, self.y = quadratic_bezier(
            self.curve_points[0],
            self.curve_points[1],
            self.curve_points[2],
            t
        )

        # Debug: show movement
        #print(f"t={t:.2f}, moved from ({old_x:.1f}, {old_y:.1f}) to ({self.x:.1f}, {self.y:.1f})")

        self.lifespan -= 1
        if self.lifespan == 0:
            self.remove()