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
    
    def draw(self, x=0, y=0):
        t.penup()
        t.goto(x, y - self.radius)
        t.pendown()
        t.color(self.color)
        t.setheading(0)
        t.begin_fill()
        t.circle(self.radius)
        t.end_fill()
        
class Neutron:
    def __init__(self):
        self.charge = 0
        self.mass = 1.008665
        self.color = "green"
        self.radius = 12
    
    def draw(self, x=0, y=0):
        t.penup()
        t.goto(x, y - self.radius)
        t.pendown()
        t.color(self.color)
        t.setheading(0)
        t.begin_fill()
        t.circle(self.radius)
        t.end_fill()
        
class Electron:
    def __init__(self):
        self.charge = -1
        self.mass = 0.00054858
        self.color = "blue"
        self.radius = 5
    
    def draw(self, distance, angle, cx=0, cy=0):
        # static draw (kept for backwards compatibility)
        x = cx + distance * math.cos(math.radians(angle))
        y = cy + distance * math.sin(math.radians(angle))
        t.penup()
        t.goto(x, y - self.radius)
        t.pendown()
        t.color(self.color)
        t.setheading(0)
        t.begin_fill()
        t.circle(self.radius)
        t.end_fill()

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
    def __init__(self, protons, neutrons):
        self.protons = protons
        self.neutrons = neutrons
        # Use nucleon size from class defaults
        self.nucleon_radius = Proton().radius
        self.color = "purple"
    
    def draw(self, cx=0, cy=0):
        total = self.protons + self.neutrons

        # Estimate nucleus radius based on number of nucleons
        # Scale: sqrt(N) * nucleon_radius * factor
        # Better estimate: area-based packing → radius proportional to sqrt(N)
        factor = 2.2
        nucleus_radius = max(self.nucleon_radius * 3.0, math.sqrt(max(1, total)) * self.nucleon_radius * factor)

        # Draw nucleus background (centered at cx,cy)
        t.penup()
        t.goto(cx, cy - nucleus_radius)
        t.pendown()
        t.color(self.color)
        t.setheading(0)
        t.begin_fill()
        t.circle(nucleus_radius)
        t.end_fill()

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
            proton.draw(cx + placed[0], cy + placed[1])

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
            neutron.draw(cx + placed[0], cy + placed[1])

class Atom:
    def __init__(self, name, protons, neutrons, color):
        self.name = name
        self.nucleus = Nucleus(protons, neutrons)  # Assuming equal number of neutrons for simplicity
        self.color = color
    
    def draw_nucleus(self, cx=0, cy=0):
        self.nucleus.draw(cx, cy)
    
    def draw_orbit(self, radius, cx=0, cy=0):
        t.penup()
        t.goto(cx, cy - radius)
        t.pendown()
        t.color(self.color)
        t.circle(radius)
        t.setheading(0)
        
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

    # Hydrogen example (1 proton, 0 neutrons) to the left
    hx, hy = cx - 250, cy
    hydrogen = Atom("Hydrogen", 1, 0, "lightblue")
    hydrogen.draw_nucleus(hx, hy)
    hydrogen.draw_orbit(100, hx, hy)
    electron = Electron()
    # animated electrons will be created later
    t.penup()
    t.goto(hx, hy - 120)
    t.color("white")
    t.write("Hydrogen", align="center", font=("Arial", 12, "normal"))

    # Deuterium example (1 proton, 1 neutron)
    deuterium = Atom("Deuterium", 1, 1, "white")
    deuterium.draw_nucleus(cx, cy)
    deuterium.draw_orbit(100, cx, cy)
    t.penup()
    t.goto(cx, cy - 120)
    t.color("white")
    t.write("Deuterium", align="center", font=("Arial", 12, "normal"))


    # Tritium example (1 proton, 2 neutrons) below center
    tx, ty = cx, cy - 250
    tritium = Atom("Tritium", 1, 2, "lightgreen")
    tritium.draw_nucleus(tx, ty)
    tritium.draw_orbit(100, tx, ty)
    t.penup()
    t.goto(tx, ty - 120)
    t.color("white")
    t.write("Tritium", align="center", font=("Arial", 12, "normal"))
    
    # Helium example (2 protons, 2 neutrons) to the right
    hx2, hy2 = cx + 250, cy
    helium = Atom("Helium", 2, 2, "yellow")
    helium.draw_nucleus(hx2, hy2)
    helium.draw_orbit(100, hx2, hy2)
    t.penup()
    t.goto(hx2, hy2 - 120)
    t.color("white")
    t.write("Helium", align="center", font=("Arial", 12, "normal"))
    
    # --- Animated electrons setup using Electron class methods ---
    animated = []

    # Hydrogen electron
    e_h = Electron()
    e_h.start_orbit(hx, hy, 100, 45, 2.2, color='blue')
    animated.append(e_h)

    # Deuterium electron
    e_d = Electron()
    e_d.start_orbit(cx, cy, 100, 0, 2.0, color='blue')
    animated.append(e_d)

    # Tritium electron
    e_t = Electron()
    e_t.start_orbit(tx, ty, 100, -45, 1.8, color='blue')
    animated.append(e_t)

    # Helium electrons (two, opposite)
    e_he1 = Electron()
    e_he1.start_orbit(hx2, hy2, 100, 90, 2.5, color='blue')
    animated.append(e_he1)
    e_he2 = Electron()
    e_he2.start_orbit(hx2, hy2, 100, 270, 2.5, color='blue')
    animated.append(e_he2)

    def animate():
        for e in animated:
            e.update()
        screen.update()
        screen.ontimer(animate, 30)

    animate()
    screen.mainloop()
