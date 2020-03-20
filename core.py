import pygame, math, sys, threading, time


# OPTIONS ---------
w, h = 1400, 800
gridSize = (25, 15)
thickness = (5, 1, 1) # The thickness of the different parts at the start (Dots, X lines, Y lines)
visible = (False, True, True) # If certain parts are visible at the start (Dots, X lines, Y lines)
fontSize = 15
# -----------------


class Grid:
    def __init__(self, size, setThickness, setVisible):
        self.size = size
        self.dist = 50
        self.vel = 0.1
        self.x = [1, 0]
        self.y = [0, 1]
        # self.rot = 0
        self.setThickness = setThickness
        self.thickness = [setThickness[0], setThickness[1], setThickness[2]]
        self.setVisible = setVisible
        self.visible = [setVisible[0], setVisible[1], setVisible[2]]

    
    # Gives the opposite of the current state of option
    def check_state(self, option):
        global visibleTick
        if pygame.time.get_ticks() - visibleTick < 100:
            return option
        visibleTick = pygame.time.get_ticks()
        if option == True:
            return False
        return True


    def change(self, key):
        global neg
        global sizeTick

        # X vector
        if key[pygame.K_UP]: self.x[1] += self.vel
        if key[pygame.K_DOWN]: self.x[1] -= self.vel

        if key[pygame.K_LEFT]: self.x[0] -= self.vel
        if key[pygame.K_RIGHT]: self.x[0] += self.vel

        # Y vector
        if key[pygame.K_w]: self.y[1] += self.vel
        if key[pygame.K_s]: self.y[1] -= self.vel

        if key[pygame.K_a]: self.y[0] -= self.vel
        if key[pygame.K_d]: self.y[0] += self.vel

        # Rotation
        offset = 1.00125
        if key[pygame.K_q]: 
            self.x[0] = (self.x[0] * math.cos(0.05 * neg) - self.x[1] * math.sin(0.05 * neg)) * offset
            self.x[1] = (self.x[0] * math.sin(0.05 * neg) + self.x[1] * math.cos(0.05 * neg)) * offset
        if key[pygame.K_e]: 
            self.y[0] = (self.y[0] * math.cos(0.05 * neg) - self.y[1] * math.sin(0.05 * neg)) * offset
            self.y[1] = (self.y[0] * math.sin(0.05 * neg) + self.y[1] * math.cos(0.05* neg)) * offset
        if key[pygame.K_r]:
            self.x[0] = (self.x[0] * math.cos(0.05 * neg) - self.x[1] * math.sin(0.05 * neg)) * offset
            self.x[1] = (self.x[0] * math.sin(0.05 * neg) + self.x[1] * math.cos(0.05 * neg)) * offset
            self.y[0] = (self.y[0] * math.cos(0.05 * neg) - self.y[1] * math.sin(0.05 * neg)) * offset
            self.y[1] = (self.y[0] * math.sin(0.05 * neg) + self.y[1] * math.cos(0.05* neg)) * offset

        # Thickness
        if key[pygame.K_1] and pygame.time.get_ticks() - sizeTick > 100:
            sizeTick = pygame.time.get_ticks()
            if neg == 1: neg = -1
            elif neg == -1: neg = 1

        if key[pygame.K_2]: self.thickness[0] += 1 * neg 
        if key[pygame.K_3]: self.thickness[1] += 1 * neg 
        if key[pygame.K_4]: self.thickness[2] += 1 * neg 

        # Visible on/off
        if key[pygame.K_5]: self.visible[0] = self.check_state(self.visible[0])
        if key[pygame.K_6]: self.visible[1] = self.check_state(self.visible[1])
        if key[pygame.K_7]: self.visible[2] = self.check_state(self.visible[2])

        # Resets 
        if key[pygame.K_8]: 
            for i in range(0, 3):
                self.thickness[i] = self.setThickness[i]
        if key[pygame.K_9]: 
            for i in range(0, 3): 
                self.visible[i] = self.setVisible[i]
        if key[pygame.K_0]: self.x = [1, 0]; self.y = [0, 1]


# Variables
pygame.init()
w, h = 1400, 800; cx, cy = w // 2, h // 2; neg = 1;
screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
pygame.display.set_caption("Linear Algebra")
font = pygame.font.SysFont(name="candara", size=fontSize, bold=1, italic=1)
clock = pygame.time.Clock()

# Grid object
grid = Grid(gridSize, thickness, visible)

# Make sure the grid has a center dot
if grid.size[0] % 2 == 0 or grid.size[1] % 2 == 0:
    print("Grid does not have a center!")
    sys.exit()


# Renders the image
def render():
    screen.fill((0, 0, 0))
    points = []

    for y in range(0, grid.size[1]):
        for x in range(0, grid.size[0]):
            
            # Creates the positions for the vectors
            vector = (math.ceil(grid.size[0] / 2) - grid.size[0] + x, math.ceil(grid.size[1] / 2) - grid.size[1] + y) 
            newVector = (vector[0] * grid.x[0] + vector[1] * grid.y[0], vector[0] * grid.x[1] + vector[1] * grid.y[1])
            Xposition = int(cx + grid.dist * newVector[0])
            Yposition = int(cy - grid.dist * newVector[1])

            # Xposition = int(((cx - grid.dist / 2 * (grid.size[0] - 1)) + grid.dist * x) * )
            # Yposition = int((cy - grid.dist / 2 * (grid.size[1] - 1)) + grid.dist * y)
            points.append((Xposition, Yposition))

            # Dots / vectors
            if grid.visible[0] == True:
                try:
                    pygame.draw.circle(screen, (0, 150, 255), (Xposition, Yposition), int(grid.thickness[0]))
                except:
                    pass 
            
            # X axis lines
            color = (0, 150, 255)
            index = grid.size[0] * y + x
            try:
                if index % grid.size[0] != 0:
                    if vector == (1, 0):
                        color = (255, 0, 0)
                    if grid.visible[1] == True: 
                        try:
                            pygame.draw.line(screen, color, points[index - 1], points[index], int(grid.thickness[1]))
                        except:
                            pass    
            except:
                pass

            # Y axis lines
            color = (0, 150, 255)
            try:
                if vector == (0, 1):
                    color = (0, 255, 0)
                if grid.visible[2] == True:
                    try:
                        pygame.draw.line(screen, color, points[index - grid.size[0]], points[index], int(grid.thickness[2])) 
                    except:
                        pass    
            except:
                pass
    
    # Text
    negText = font.render(f"[1] neg: {neg}", 1, (255, 255, 255))
    thicknessText = font.render(f"[2 3 4] Thickness: ({grid.thickness[0]}, {grid.thickness[1]}, {grid.thickness[2]})", 1, (255, 255, 255))
    visibleText = font.render(f"[5 6 7] Visible: ({grid.visible[0]}, {grid.visible[1]}, {grid.visible[2]})", 1, (255, 255, 255))
    resetText = font.render(f"[8 9 0] Reset: (Thickness, Visibility, Vectors)", 1, (255, 255, 255))
    exitText = font.render(f"[esc] Close program", 1, (255, 255, 255))           
    screen.blit(negText, (w - fontSize * 16.4, fontSize * 0))
    screen.blit(thicknessText, (w - fontSize * 18, fontSize * 1))
    screen.blit(visibleText, (w - fontSize * 18, fontSize * 2))
    screen.blit(resetText, (w - fontSize * 18.15, fontSize * 3))
    screen.blit(exitText, (w - fontSize * 17.5, fontSize * 4))

    pygame.display.update()


# Different clocks for delays
tick = pygame.time.get_ticks()
sizeTick = pygame.time.get_ticks()
visibleTick = pygame.time.get_ticks()

while True:
    clock.tick(60)
    key = pygame.key.get_pressed()

    # Exit
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            w, h = event.w, event.h; cx, cy = w // 2, h // 2;
            screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        if event.type == pygame.QUIT:
            break

    if key[pygame.K_ESCAPE]:
        break 

    # Grid
    grid.change(key)

    render()

    # Extra
    if True:
        pass
    elif pygame.time.get_ticks() - tick > 1500: # Change this if statement, if you want to get the values of X and Y
        tick = pygame.time.get_ticks()
        print("X")
        print("    " + str(grid.x[0]))
        print("    " + str(grid.x[1]))
        print("Y")
        print("    " + str(grid.y[0]))
        print("    " + str(grid.y[1]))
        print("-------------------------")   
