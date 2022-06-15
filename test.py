import random
from random import randint

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

import matplotlib

matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

import pylab

colors = [["#e6f7ff"], ["#99ddff"], ["#33ccff"], ["#6666ff"], ["#0099ff"],
          ["#0066ff"], ["#3366ff"], ["#0044cc"], ["#000099"], ["#000066"],]
coord = []
color = (100, 100, 50)
map_radius = 4
for q in range(-map_radius, map_radius+1):
    r1 = max(-map_radius, -q - map_radius)
    r2 = min(map_radius, -q + map_radius);
    for r in range(r1, r2+1):
        coord.append([q, r, -q - r])
        print([q, r, -q - r])
        # colors.append(rhinoscriptsytnax.CreateColor(q, r, -q - r) )

# Horizontal cartesian coords
hcoord = [c[0] for c in coord]
print(hcoord)
# Vertical cartersian coords
vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in coord]
print(vcoord)
for i in range(len(vcoord)):
    temp = vcoord[i]
    vcoord[i] = -hcoord[i]
    hcoord[i] = temp

fig, ax = plt.subplots(1, figsize=(5, 5))
ax.set_aspect('equal')

# Add some coloured hexagons
for x, y in zip(hcoord, vcoord):
    color = random.choice(colors)[0]

    hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3,
                         orientation=np.radians(120), facecolor=color,
                         alpha=0.9, edgecolor='k')
    ax.add_patch(hex)

ax.scatter(hcoord, vcoord, alpha=0.2)

ax = fig.gca()
# ax.plot([1, 2, 4])

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()

import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((600, 600), DOUBLEBUF)
screen = pygame.display.get_surface()

size = canvas.get_width_height()
print(size)
surf = pygame.image.fromstring(raw_data, size, "RGB")
screen.blit(surf, (50, 50))
pygame.display.flip()

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
