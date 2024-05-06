import pygame
import numpy as np
import math
from math import *

rotation_z = 0
rotation_y = 0
rotation_x = 0

offset_x = 0
offset_y = -1
offset_z = 0
projected_points = []
counter = 0
WIDTH, HEIGHT = 800, 600
scale = 150
dot_pos = [WIDTH/2, HEIGHT/2]
globalAngle = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
clock = pygame.time.Clock()

pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

points = []
points.append(np.matrix([int(0 + offset_x), int(1 + offset_y), int(0 + offset_z)]))
points.append(np.matrix([int(-1 + offset_x), int(0 + offset_y), int(-1 + offset_z)]))
points.append(np.matrix([int(-1 + offset_x), int(0 + offset_y), int(-1 + offset_z)]))
points.append(np.matrix([int(1 + offset_x), int(0 + offset_y), int(1 + offset_z)]))
points.append(np.matrix([int(1 + offset_x), int(0 + offset_y), int(-1 + offset_z)]))

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])


def rotate_z(angle):
    global rotation_z
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])
    return rotation_z

def rotate_y(angle):
    global rotation_y
    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])
    return rotation_y

def rotate_x(angle):
    global rotation_x
    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    return rotation_x 

def project():
    for point in points:
        reshaped = point.reshape((3, 1))
        rotated2d = np.dot(rotate_y(globalAngle), reshaped)
        rotated2d = np.dot(rotate_x(globalAngle), rotated2d)
        rotated2d = np.dot(rotate_z(globalAngle), rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)
        x = int(projected2d[0][0] * scale) + dot_pos[0]
        y = int(projected2d[1][0] * scale) + dot_pos[1]
        pygame.draw.circle(screen, WHITE, (x, y), 5)
        
        projected_points.append([x, y])
        global counter
        counter += 1
        if len(projected_points) > 1:
            for i in range(len(projected_points)):
                pygame.draw.line(screen, WHITE, (projected_points[i][0], projected_points[i][1]), (projected_points[counter-1][0], projected_points[counter-1][1]))

            

while True:
    #the main updater
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    
    #draw background
    screen.fill(BLACK) 
    #draw the projection
    projected_points = []
    project()
    
    #change global angle change
    globalAngle += 0.005

    counter = 0
    #update display
    pygame.display.update()


