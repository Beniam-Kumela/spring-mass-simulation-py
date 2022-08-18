#import modules
from vpython import *

#create start and stop button
running = True
def run(self):
    global running, remember_dt, dt
    running = not running
    if running:
        self.text = "Pause"
        dt = remember_dt
    else:
        self.text = "Run"
        remember_dt = dt
        dt = 0
    return
button(text = "Pause", pos=scene.title_anchor, bind=run)

#create reset button
def reset(self):
    global t, mass, spring, eq_pos, mass_mass, kinetic_friction, spring_constant
    t = 0
    spring.axis = vector(5, 0, 0)
    mass.pos = vector(-7, 0, 0)
    mass.velocity = vector(0.1, 0, 0)
    mass.force = vector(0, 0, 0)
    eq_pos.x = -9
    mass_mass = 1
    kinetic_friction = 0
    spring_constant = 1
    spring.thickness = 0.025
    g1.delete()
    g2.delete()
    g3.delete()


button(text="Reset", pos=scene.title_anchor, bind=reset)

#create amplitude slider
def setamplitude(self):
    global eq_pos
    wt.text = "Amplitude = "+'{:1.2f}'.format(self.value)
    eq_pos.x = (-self.value)-7


amplitude = slider(min=0.1, max=2.2, value=2, bind=setamplitude)
wt = wtext(text="Amplitude = "+'{:1.2f}'.format(amplitude.value))
scene.append_to_caption("\n \n")

#create mass slider
def setmass(self):
    global mass_mass
    wt2.text = "Mass = "+'{:1.2f}'.format(self.value)
    mass_mass = self.value


mass = slider(min=0.1, max=5, value=1, bind=setmass)
wt2 = wtext(text="Mass = "+'{:1.2f}'.format(mass.value))
scene.append_to_caption("\n \n")

#create friction slider
def setfriction(self):
    global kinetic_friction
    wt3.text = "\u03BC\u2096 = "+'{:1.3f}'.format(self.value)
    kinetic_friction = self.value


friction = slider(min=0, max=0.1, value=0, step=0.001, bind=setfriction)
wt3 = wtext(text="\u03BC\u2096 = "+'{:1.3f}'.format(friction.value))
scene.append_to_caption("\n \n")

#create spring constant slider
def setspringconstant(self):
    global spring_constant, spring
    wt4.text = "k = "+'{:1.2f}'.format(self.value)
    spring_constant = self.value
    spring.thickness = self.value*(0.025)

k = slider(min=0.25, max=10, value=1, bind=setspringconstant)
wt4 = wtext(text="k = "+'{:1.2f}'.format(k.value))
scene.append_to_caption("\n \n")

#load in objects from vpython
wallL = box(
    pos=vector(-12, 0, 0), size=vector(0.2, 12, 12)
)
spring = helix(
    pos=wallL.pos, axis=vector(5, 0, 0), radius=0.5
)
mass = box(
    size=vector(1, 1, 1), pos=wallL.pos + spring.axis, color=color.yellow, opacity=1, velocity=vector(0.1, 0, 0), force=vector(0, 0, 0)
)
floor = box(
    pos=vector(-6.1, -3.5, 0), size=vector(12, 6, 12)
)

#set initial parameters
xgraph = graph(title="Mass position (\u0394 x) vs Time (s)", xtitle="Time (s)", ytitle="Mass position (\u0394 x)")
g1 = gcurve(color=color.blue)
ugraph = graph(title="Potential Energy (J) vs Time (s)", xtitle="Time (s)", ytitle="Potential Energy (J)")
g2 = gcurve(color=color.green)
kgraph = graph(title="Kinetic Energy (J) vs Time (s)", xtitle="Time (s)", ytitle="Kinetic Energy (J)")
g3 = gcurve(color=color.red)
eq_pos = vector(-9, 0, 0)
t = 0
dt = 0.01
kinetic_friction = 0
spring_constant = 1
mass_mass = 1
g=9.8

#physics of the damped oscillator
while True:
    rate(100)
    acceleration = (eq_pos - mass.pos) * spring_constant/mass_mass - (kinetic_friction*mass_mass*g*mass.velocity)
    mass.velocity = mass.velocity + acceleration * dt
    mass.pos = mass.pos + mass.velocity * dt
    spring.axis = mass.pos - spring.pos
    t = t + dt
    g1.plot(t, (mass.pos.x + abs(eq_pos.x)))
    g2.plot(t, (0.5*((abs(eq_pos.x - mass.pos.x))**2)*spring_constant))
    g3.plot(t, (0.5*mass_mass*(mass.velocity.x**2)))