import turtle
import random
import math

t = turtle.Turtle()

t.screen.bgcolor("black")
t.color("white")
t.speed(100)

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
        t.penup()
        t.goto(cx, cy)
        t.setheading(angle)
        t.forward(distance)
        t.pendown()
        t.color(self.color)
        t.begin_fill()
        t.circle(self.radius)
        t.end_fill()

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
        t.setheading(0)
        t.color(self.color)
        t.circle(radius)
        
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
    electron.draw(100, 45, hx, hy)
    t.penup()
    t.goto(hx, hy - 120)
    t.color("white")
    t.write("Hydrogen", align="center", font=("Arial", 12, "normal"))

    # Deuterium example (1 proton, 1 neutron)
    deuterium = Atom("Deuterium", 1, 1, "white")
    deuterium.draw_nucleus(cx, cy)
    deuterium.draw_orbit(100, cx, cy)
    electron.draw(100, 0, cx, cy)
    t.penup()
    t.goto(cx, cy - 120)
    t.color("white")
    t.write("Deuterium", align="center", font=("Arial", 12, "normal"))


    # Tritium example (1 proton, 2 neutrons) below center
    tx, ty = cx, cy - 250
    tritium = Atom("Tritium", 1, 2, "lightgreen")
    tritium.draw_nucleus(tx, ty)
    tritium.draw_orbit(100, tx, ty)
    electron.draw(100, -45, tx, ty)
    t.penup()
    t.goto(tx, ty - 120)
    t.color("white")
    t.write("Tritium", align="center", font=("Arial", 12, "normal"))
    
    # Helium example (2 protons, 2 neutrons) to the right
    hx2, hy2 = cx + 250, cy
    helium = Atom("Helium", 2, 2, "yellow")
    helium.draw_nucleus(hx2, hy2)
    helium.draw_orbit(100, hx2, hy2)    
    electron.draw(100, 90, hx2, hy2)
    electron.draw(100, 270, hx2, hy2)
    t.penup()
    t.goto(hx2, hy2 - 120)
    t.color("white")
    t.write("Helium", align="center", font=("Arial", 12, "normal"))
    
    t.goto(1000,1000)  # Move turtle out of the way
    turtle.done()
