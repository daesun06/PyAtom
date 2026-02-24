import turtle
import random
import math

screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.color("white")
t.speed(0)

class Proton:
    def __init__(self):
        self.charge = +1
        self.mass = 1.007276
        self.color = "red"
        self.radius = 12
    
    def draw(self, x=0, y=0, drawer=None):
        drawer = drawer or t
        drawer.penup()
        drawer.goto(x, y - self.radius)
        drawer.pendown()
        drawer.color(self.color)
        drawer.setheading(0)
        drawer.begin_fill()
        drawer.circle(self.radius)
        drawer.end_fill()
        
class Neutron:
    def __init__(self):
        self.charge = 0
        self.mass = 1.008665
        self.color = "green"
        self.radius = 12
    
    def draw(self, x=0, y=0, drawer=None):
        drawer = drawer or t
        drawer.penup()
        drawer.goto(x, y - self.radius)
        drawer.pendown()
        drawer.color(self.color)
        drawer.setheading(0)
        drawer.begin_fill()
        drawer.circle(self.radius)
        drawer.end_fill()
        
class Electron:
    def __init__(self):
        self.charge = -1
        self.mass = 0.00054858
        self.color = "blue"
        self.radius = 5
    
    def draw(self, distance, angle, cx=0, cy=0, drawer=None):
        # static draw (kept for backwards compatibility)
        drawer = drawer or t
        x = cx + distance * math.cos(math.radians(angle))
        y = cy + distance * math.sin(math.radians(angle))
        drawer.penup()
        drawer.goto(x, y - self.radius)
        drawer.pendown()
        drawer.color(self.color)
        drawer.setheading(0)
        drawer.begin_fill()
        drawer.circle(self.radius)
        drawer.end_fill()

    # Animation helper creates an independent turtle for animation
    def create_anim_turtle(self):
        et = turtle.Turtle()
        et.hideturtle()
        et.penup()
        et.speed(0)
        return et

    # Start orbit animation for this electron
    def start_orbit(self, cx, cy, r, angle, speed, color=None):
        self.orbit_cx = cx
        self.orbit_cy = cy
        self.r = r
        self.angle = angle
        self.speed = speed
        self.anim_color = color or self.color
        self.anim_turtle = self.create_anim_turtle()

    # Update position for animation frame
    def update(self):
        # advance angle
        self.angle = (self.angle + self.speed) % 360
        rad = math.radians(self.angle)
        x = self.orbit_cx + self.r * math.cos(rad)
        y = self.orbit_cy + self.r * math.sin(rad)
        # draw dot at new position
        self.anim_turtle.clear()
        self.anim_turtle.goto(x, y)
        self.anim_turtle.dot(self.radius * 2, self.anim_color)

class Nucleus:
    def __init__(self, protons, neutrons, scale=1.0):
        self.protons = protons
        self.neutrons = neutrons
        # Use nucleon size from class defaults
        self.nucleon_radius = Proton().radius
        self.color = "purple"
        # allow compact / expanded nucleus by scale factor
        self.scale = float(scale)
    
    def draw(self, cx=0, cy=0, drawer=None):
        drawer = drawer or t
        total = self.protons + self.neutrons

        # Estimate nucleus radius based on number of nucleons
        # Scale: sqrt(N) * nucleon_radius * factor
        # Better estimate: area-based packing → radius proportional to sqrt(N)
        factor = 2.2 * self.scale
        nucleus_radius = max(self.nucleon_radius * 3.0 * self.scale, math.sqrt(max(1, total)) * self.nucleon_radius * factor)

        # Draw nucleus background (centered at cx,cy)
        drawer.penup()
        drawer.goto(cx, cy - nucleus_radius)
        drawer.pendown()
        drawer.color(self.color)
        drawer.setheading(0)
        drawer.begin_fill()
        drawer.circle(nucleus_radius)
        drawer.end_fill()

        # Place nucleons randomly inside nucleus without overlapping
        positions = []
        min_dist = self.nucleon_radius * 2 * 0.9

        def try_place():
            # uniform distribution inside circle
            a = random.random()
            r = math.sqrt(a) * (nucleus_radius - self.nucleon_radius)
            theta = random.uniform(0, 2 * math.pi)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            for px, py in positions:
                if math.hypot(px - x, py - y) < min_dist:
                    return None
            return (x, y)

        # place protons
        for i in range(self.protons):
            placed = None
            for _ in range(1000):
                p = try_place()
                if p:
                    placed = p
                    break
            if not placed:
                placed = (0, 0)
            positions.append(placed)
            proton = Proton()
            # offset by nucleus center
            proton.draw(cx + placed[0], cy + placed[1], drawer=drawer)

        # place neutrons
        for i in range(self.neutrons):
            placed = None
            for _ in range(1000):
                p = try_place()
                if p:
                    placed = p
                    break
            if not placed:
                placed = (0, 0)
            positions.append(placed)
            neutron = Neutron()
            # offset by nucleus center
            neutron.draw(cx + placed[0], cy + placed[1], drawer=drawer)

    def radius(self):
        # same formula as in draw to compute nucleus radius
        total = self.protons + self.neutrons
        factor = 2.2 * self.scale
        return max(self.nucleon_radius * 3.0 * self.scale, math.sqrt(max(1, total)) * self.nucleon_radius * factor)

    def mass(self):
        # approximate mass proportional to nucleon count
        return max(1.0, float(self.protons + self.neutrons))

class Atom:
    def __init__(self, name, protons, neutrons, color, cx=0, cy=0, nucleus_scale=1.0):
        self.name = name
        self.nucleus = Nucleus(protons, neutrons, scale=nucleus_scale)
        self.color = color
        self.cx = cx
        self.cy = cy
        # per-atom drawing turtle so nucleus/orbit can be cleared/redrawn
        self.drawer = turtle.Turtle()
        self.drawer.hideturtle()
        self.drawer.penup()
        self.drawer.speed(0)
        self.electrons = []
        self.vx = 0.0
        self.vy = 0.0

    def add_electron(self, r, angle, speed, color=None):
        e = Electron()
        e.start_orbit(self.cx, self.cy, r, angle, speed, color=color)
        self.electrons.append(e)
        return e

    def start_motion(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def start_random_motion(self, max_speed=1.0):
        self.vx = random.uniform(-max_speed, max_speed)
        self.vy = random.uniform(-max_speed, max_speed)

    def update(self):
        # move
        self.cx += self.vx
        self.cy += self.vy

        # bounce within window bounds
        w = screen.window_width() / 2
        h = screen.window_height() / 2
        margin = 60
        if self.cx > w - margin:
            self.cx = w - margin
            self.vx *= -1
        if self.cx < -w + margin:
            self.cx = -w + margin
            self.vx *= -1
        if self.cy > h - margin:
            self.cy = h - margin
            self.vy *= -1
        if self.cy < -h + margin:
            self.cy = -h + margin
            self.vy *= -1

        # redraw nucleus and orbits
        self.drawer.clear()
        # draw orbits for each unique electron radius
        radii = sorted({e.r for e in self.electrons})
        for r in radii:
            self.drawer.penup()
            self.drawer.goto(self.cx, self.cy - r)
            self.drawer.pendown()
            self.drawer.color(self.color)
            self.drawer.setheading(0)
            self.drawer.circle(r)
            self.drawer.penup()
        # draw nucleus (uses drawer for nucleons)
        self.nucleus.draw(self.cx, self.cy, drawer=self.drawer)
        # label
        self.drawer.penup()
        self.drawer.goto(self.cx, self.cy - 120)
        self.drawer.color('white')
        self.drawer.write(self.name, align="center", font=("Arial", 12, "normal"))

        # update electron orbit centers
        for e in self.electrons:
            e.orbit_cx = self.cx
            e.orbit_cy = self.cy
        
# Example usage
if __name__ == "__main__":
    coords = input("Enter atom center coordinates as 'x,y' (default 0,0): ").strip()
    if coords:
        try:
            cx, cy = [float(s) for s in coords.split(",")]
        except Exception:
            print("Invalid input, using 0,0")
            cx, cy = 0, 0
    else:
        cx, cy = 0, 0

    atoms = []

    # Hydrogen example (1 proton, 0 neutrons) to the left
    hx, hy = cx - 250, cy
    hydrogen = Atom("Hydrogen", 1, 0, "lightblue", hx, hy)
    hydrogen.add_electron(100, 45, 20.0, color='cyan')
    hydrogen.start_random_motion(0.9)
    atoms.append(hydrogen)

    # Deuterium example (1 proton, 1 neutron)
    deuterium = Atom("Deuterium", 1, 1, "white", cx, cy)
    deuterium.add_electron(100, 0, 20.0, color='cyan')
    deuterium.start_random_motion(0.9)
    atoms.append(deuterium)

    # Tritium example (1 proton, 2 neutrons) below center
    tx, ty = cx, cy - 250
    tritium = Atom("Tritium", 1, 2, "lightgreen", tx, ty)
    tritium.add_electron(100, -45, 20.0, color='cyan')
    tritium.start_random_motion(1.0)
    atoms.append(tritium)
    
    # Helium example (2 protons, 2 neutrons) to the right
    hx2, hy2 = cx + 250, cy
    helium = Atom("Helium", 2, 2, "yellow", hx2, hy2)
    helium.add_electron(100, 90, 20.0, color='cyan')
    helium.add_electron(100, 270, 20.0, color='cyan')
    helium.start_random_motion(1.3)
    atoms.append(helium)

    # Ferrum (Iron) example with compact core and multiple electron shells
    # Ferrum: Z=26, choose typical isotope around 56 nucleons
    fx, fy = cx, cy + 250
    ferrum = Atom("Ferrum", 26, 30, "orange", fx, fy, nucleus_scale=0.5)
    # electron shells (approx): 2,8,14,2 -> distribute electrons evenly per shell
    shells = [(140, 2), (180, 8), (220, 14), (260, 2)]
    for r, count in shells:
        for k in range(count):
            angle = k * (360.0 / max(1, count))
            # vary speed slightly per shell
            speed = 500.0  # random.uniform(1.0, 3.0) * (1.0 + (r / 200.0))
            ferrum.add_electron(r, angle, speed, color='cyan')
    # give ferrum a slight drift so it moves and can collide
    ferrum.start_random_motion(0.6)
    atoms.append(ferrum)
    
    

    # collect animated electrons for frame updates
    animated = []
    for a in atoms:
        for e in a.electrons:
            animated.append(e)

    def animate():
        for a in atoms:
            a.update()

        # detect and resolve nucleus collisions between atoms
        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):
                a = atoms[i]
                b = atoms[j]
                dx = a.cx - b.cx
                dy = a.cy - b.cy
                dist = math.hypot(dx, dy)
                r1 = a.nucleus.radius()
                r2 = b.nucleus.radius()
                if dist <= 0:
                    # jitter a tiny bit to avoid divide by zero
                    dx = random.uniform(-0.5, 0.5)
                    dy = random.uniform(-0.5, 0.5)
                    dist = math.hypot(dx, dy)
                if dist < (r1 + r2):
                    # normalized collision axis
                    nx = dx / dist
                    ny = dy / dist
                    # relative velocity along normal
                    rvx = a.vx - b.vx
                    rvy = a.vy - b.vy
                    vel_along = rvx * nx + rvy * ny
                    # only resolve if moving towards each other (or overlapping)
                    m1 = a.nucleus.mass()
                    m2 = b.nucleus.mass()
                    e = 1.0
                    # compute impulse scalar
                    j = -(1 + e) * vel_along / (1.0 / m1 + 1.0 / m2)
                    # apply impulse
                    a.vx += (j * nx) / m1
                    a.vy += (j * ny) / m1
                    b.vx -= (j * nx) / m2
                    b.vy -= (j * ny) / m2
                    # separate overlapping atoms proportionally to mass
                    overlap = (r1 + r2) - dist
                    if overlap > 0:
                        a.cx += nx * (overlap * (m2 / (m1 + m2)))
                        a.cy += ny * (overlap * (m2 / (m1 + m2)))
                        b.cx -= nx * (overlap * (m1 / (m1 + m2)))
                        b.cy -= ny * (overlap * (m1 / (m1 + m2)))

        for e in animated:
            e.update()
        screen.update()
        screen.ontimer(animate, 30)

    animate()
    screen.mainloop()
