import pygame
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import matplotlib.backends.backend_agg as agg

import random

MAP_RADIUS = 4

class Grid:
    def __init__(self,data):
        """
        This function runs one time only before we begin the process
        """
        pygame.init()
        self.window = pygame.display.set_mode((600, 600), pygame.DOUBLEBUF)
        self.screen = pygame.display.get_surface()
        self.data=data
        self.canvas, self.raw_data = self.create_grid(data)  # Fix this
        self.size = self.canvas.get_width_height()
        print(self.size)
        self.count = 0

        self.surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        self.text = self.font.render('generation: ' + str(self.count), True, "pink")
        # textRect = text.get_rect()
        # textRect.center = (600 // 2, 25)
        # screen.blit(text, (100, 100))
        self.screen.blit(self.surf, (50, 50))
        self.textRect = self.text.get_rect()
        self.textRect.center = (600 // 2, 25)
        pygame.display.flip()
        self.crashed = False

    def draw_grid(self, colors):
        """
        This function runs evey iteration and should draw the grid with the new colors.
        Colors: dictionary from coord to color id.
        For example:
         {
            (3, -4, 1): 1,
            (3, -3, 0): 3,
            (1, -3, 2): 8,
            (4, -4, 0): 3,
            ...
        }

        Notice:
        Not every coord has a color (because it wasn't selected as a representitive). Keep it blanc?

        """


        # for row in data:
        #     pixel_i, pixel_j = choose_representative(row, grid)
        #     correct_pixel_neighborhood(row, pixel_i, pixel_j)
        #     pygame.display.update()
        #
        #     total_score = calc_total_score()
        #     if total_score < MIN_SCORE:
        #         break
        self.screen.fill("white")
        self.count += 1
        self.canvas, self.raw_data = self.create_grid(self.data)
        self.surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")
        self.text = self.font.render('generation: ' + str(self.count), False, "pink")
        print(self.count)
        self.screen.blit(self.surf, (50, 50))
        self.screen.blit(self.text, self.textRect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.crashed = True
        pygame.display.update()

    def create_grid(self, grid):
        plt.close()
        colors = [["#e6f7ff"], ["#99ddff"], ["#33ccff"], ["#6666ff"], ["#0099ff"],
                  ["#0066ff"], ["#3366ff"], ["#0044cc"], ["#000099"], ["#000066"], ]
        coord = []
        color = (100, 100, 50)
        map_radius = 4
        for q in range(-map_radius, map_radius + 1):
            r1 = max(-map_radius, -q - map_radius)
            r2 = min(map_radius, -q + map_radius);
            for r in range(r1, r2 + 1):
                coord.append([q, r, -q - r])
                # colors.append(rhinoscriptsytnax.CreateColor(q, r, -q - r) )

        # Horizontal cartesian coords
        hcoord = [c[0] for c in coord]
        # Vertical cartersian coords
        vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in coord]
        for i in range(len(vcoord)):
            temp = vcoord[i]
            vcoord[i] = -hcoord[i]
            hcoord[i] = temp

        fig, ax = plt.subplots(1, figsize=(5, 5))
        ax.set_aspect('equal')

        # Add some coloured hexagons
        for x, y in zip(hcoord, vcoord):
            # todo: color by grid.eco
            color = random.choice(colors)[0]
            # color=grid[x]
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
        return [canvas, raw_data]