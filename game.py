import pygame
from random import randint, random
from colorsys import rgb_to_hsv, hsv_to_rgb
def colorer(base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
    # If only color_variance_red is filled, use it for all channels and apply the same diff to all
    if color_variance_green is None and color_variance_blue is None:
        diff = randint(-color_variance_red, color_variance_red)
        r = max(0, min(255, base_r + diff))
        g = max(0, min(255, base_g + diff))
        b = max(0, min(255, base_b + diff))
        # Clamp negative values to positive, and if any channel >255, reset all to base color
        if r < 0 or g < 0 or b < 0:
            r, g, b = abs(r), abs(g), abs(b)
        if r > 255:
            r = base_r
        if g > 255:
            g = base_g
        if b > 255:
            b = base_b
    else:
        # Apply variance per channel
        if color_variance_green is None:
            color_variance_green = color_variance_red
        if color_variance_blue is None:
            color_variance_blue = color_variance_red

        diff_r = randint(-color_variance_red, color_variance_red)
        diff_g = randint(-color_variance_green, color_variance_green)
        diff_b = randint(-color_variance_blue, color_variance_blue)
        
        r = max(0, min(255, base_r + diff_r))
        g = max(0, min(255, base_g + diff_g))
        b = max(0, min(255, base_b + diff_b))
        # Clamp negative values to positive, and if any channel >255, reset all to base color
        if r < 0 or g < 0 or b < 0:
            r, g, b = abs(r), abs(g), abs(b)
        if r > 255:
            r = base_r
        if g > 255:
            g = base_g
        if b > 255:
            b = base_b
    return (r, g, b)




class Particle:
    """Base class for all particles"""
    def __init__(self, base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
        self.has_moved = False
        self.base_color = (base_r, base_g, base_b)
        # If only color_variance_red is filled, use it for all channels and apply the same diff to all
        self.color = colorer(base_r, base_g, base_b, color_variance_red, color_variance_green, color_variance_blue) 
        self.spawn_color = self.color
    def __repr__(self):
        return self.__class__.__name__
    
    def move(self, grid, old_y, old_x, new_y, new_x):
        grid[new_y][new_x], grid[old_y][old_x] = grid[old_y][old_x], grid[new_y][new_x]

class Static(Particle):
    """Base class for particles that don't move"""
    def __init__(self, base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
        super().__init__(base_r, base_g, base_b, color_variance_red, color_variance_green, color_variance_blue)

class StraightFalling(Particle):
    """Base class for particles that fall straight down"""
    def __init__(self, base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
        super().__init__(base_r, base_g, base_b, color_variance_red, color_variance_green, color_variance_blue)
    
    def check_movement(self, x, y, grid):
        return self.check_below(x, y, grid)

    def check_below(self, x, y, grid):
        if y >= height - 1:
            return False
        if isinstance(grid[y+1][x], (empty, Liquid, LightGas)):
            self.move(grid, y, x, y+1, x)
            return True
        return False

class Granular(Particle):
    """Base class for sand-like particles that fall and slide"""
    def __init__(self, base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
        super().__init__(base_r, base_g, base_b, color_variance_red, color_variance_green, color_variance_blue)

    def check_movement(self, x, y, grid):
        return self.check_below(x, y, grid)

    def check_bottom_left(self, x, y, grid, other):
        # Left edge check
        if x <= 0:
            if other == True:
                return False
            else:
                return self.check_bottom_right(x, y, grid, True)
        # Regular checks
        if isinstance(grid[y+1][x-1], (empty, Liquid, LightGas)):
            self.move(grid, y, x, y+1, x-1)
            return True
        else:
            if other == True:
                return False
            else:
                return self.check_bottom_right(x, y, grid, True)

    def check_bottom_right(self, x, y, grid, other):
        # Right edge check
        if x >= width - 1:
            if other == True:
                return False
            else:
                return self.check_bottom_left(x, y, grid, True)
        # Regular checks
        if isinstance(grid[y+1][x+1], (empty, Liquid, LightGas)):
            self.move(grid, y, x, y+1, x+1)
            return True
        else:
            if other == True:
                return False
            else:
                return self.check_bottom_left(x, y, grid, True)

    def check_below(self, x, y, grid):
        # Floor check
        if y >= height - 1:
            return False
        # Regular checks
        if isinstance(grid[y+1][x], (empty, Liquid, LightGas)):
            self.move(grid, y, x, y+1, x)
            return True
        else:
            rnder = randint(0,1)
            if rnder == 0:
                return self.check_bottom_left(x, y, grid, False)
            else:
                return self.check_bottom_right(x, y, grid, False)

class Liquid(Particle):
    """Base class for liquid particles that fall, slide, and flow horizontally"""
    def __init__(self, base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
        super().__init__(base_r, base_g, base_b, color_variance_red, color_variance_green, color_variance_blue)

    def check_movement(self, x, y, grid):
        return self.check_below(x, y, grid)
    
    def check_bottom_left(self, x, y, grid, other):
        # Left edge check
        if x <= 0:
            if other == True:
                return False
            else:
                return self.check_bottom_right(x, y, grid, True)
        # Regular checks
        if isinstance(grid[y+1][x-1], (empty,LightGas)):
            self.move(grid, y, x, y+1, x-1)
            return True
        else:
            if other == True:
                return False
            else:
                return self.check_bottom_right(x, y, grid, True)

    def check_bottom_right(self, x, y, grid, other):
        # Right edge check
        if x >= width - 1:
            if other == True:
                return False
            else:
                return self.check_bottom_left(x, y, grid, True)
        # Regular checks
        if isinstance(grid[y+1][x+1], (empty, LightGas)):
            self.move(grid, y, x, y+1, x+1)
            return True
        else:
            if other == True:
                if randint(0, 1) == 0:
                    return self.check_left(x, y, grid, False)
                else:
                    return self.check_right(x, y, grid, False)
            else:
                return self.check_bottom_left(x, y, grid, True)

    def check_left(self, x, y, grid, other):
        if x <= 0:
            if other == True:
                return False
            else:
                return self.check_right(x, y, grid, other)
        if isinstance(grid[y][x-1], (empty, LightGas)):
            self.move(grid, y, x, y, x-1)
            return True
        else:
            if other == True:
                return False
            else:
                return self.check_right(x, y, grid, True)
    
    def check_right(self, x, y, grid, other):
        if x >= width-1:
            if other == True:
                return False
            else:
                return self.check_left(x, y, grid, True)
        if isinstance(grid[y][x+1], (empty, LightGas)):
            self.move(grid, y, x, y, x+1)
            return True
        else:
            if other == True:
                if randint(0, 1) == 0:
                    return self.check_left(x, y, grid, False)
                else:
                    return self.check_right(x, y, grid, False)
            else:
                return self.check_left(x, y, grid, True)

    def check_below(self, x, y, grid):
        # Floor check
        if y >= height - 1:
            return False
        # Regular checks
        if isinstance(grid[y+1][x], empty):
            self.move(grid, y, x, y+1, x)
            return True
        else:
            if randint(0, 1) == 0:
                return self.check_bottom_left(x, y, grid, False)
            else:
                return self.check_bottom_right(x, y, grid, False)

class LightGas(Particle):
    def __init__(self, base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
        super().__init__(base_r, base_g, base_b, color_variance_red, color_variance_green, color_variance_blue)
    
    def check_bottom_left(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention
        # Floor check
        if y >= height - 1:
            #* At the floor of the simulation, it can't go further down.
            #* This means that it should either go left or right, instead of trying diagonally downwards like standard particles.
            #* Since this particle originally intended to go downleft, it'll try to go left.
            return self.check_left(x, y, grid, counter + 1)
        # Left edge check
        if x <= 0:
            #* At the left wall of the simulation, it can't go bottom left, top left, or left itself.
            #* This means that it should either go up or down, instead of trying the other side like standard particles.
            #* Since this particle originally intended to go downleft, it'll try to go down.
            return self.check_below(x,y, grid, counter+1)
        # Regular checks
        target=grid[y+1][x-1]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y+1, x-1)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            return self.check_below(x,y, grid, counter+1)
        
    def check_below(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention

        # Floor check
        if y >= height-1:
            #* At the floor of the simulation, it can't go further down.
            #* This means that it should either go left or right, instead of trying diagonally downwards like standard particles.
            #* Since this particle originally intended to go straight down, it'll randomly go left or right.
            if randint(0, 1) == 0:
                return self.check_left(x,y, grid, counter+1)
            else:
                return self.check_right(x,y, grid, counter+1)
        # Regular checks
        target=grid[y+1][x]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y+1, x)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            if randint(0, 1) == 0:
                return self.check_left(x,y, grid, counter+1)
            else:
                return self.check_right(x,y, grid, counter+1)
    
    def check_bottom_right(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention
        # Floor check
        if y >= height - 1:
            #* At the floor of the simulation, it can't go further down.
            #* This means that it should either go left or right, instead of trying diagonally downwards like standard particles.
            #* Since this particle originally intended to go downright, it'll try to go right.
            return self.check_right(x, y, grid, counter + 1)
        # Right edge check
        if x >= width-1:
            #* At the right wall of the simulation, it can't go bottom right, top right, or right itself.
            #* This means that it should either go up or down, instead of trying the other side like standard particles.
            #* Since this particle originally intended to go downright, it'll try to go down.
            return self.check_below(x,y, grid, counter+1)
        # Regular checks
        target=grid[y+1][x+1]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y+1, x+1)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            return self.check_below(x,y, grid, counter+1)
    
    def check_left(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention

        # Left edge check
        if x <= 0:
            #* At the left wall of the simulation, it can't go bottom left, top left, or left itself.
            #* This means that it should either go up or down, instead of trying the other side like standard particles.
            #* Since this particle had no original vertical intention, it'll randomly pick to go up or down.
            if randint(0, 1) == 0:
                return self.check_below(x,y, grid, counter+1)
            else:
                return self.check_above(x,y, grid, counter+1)
        # Regular checks
        target=grid[y][x-1]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y, x-1)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            if randint(0, 1) == 0:
                return self.check_below(x,y, grid, counter+1)
            else:
                return self.check_above(x,y, grid, counter+1)
    
    def check_right(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention

        # Right edge check
        if x >= width-1:
            #* At the right wall of the simulation, it can't go bottom right, top right, or right itself.
            #* This means that it should either go up or down, instead of trying the other side like standard particles.
            #* Since this particle had no original vertical intention, it'll randomly pick to go up or down.
            if randint(0, 1) == 0:
                return self.check_below(x,y, grid, counter+1)
            else:
                return self.check_above(x,y, grid, counter+1)
        # Regular checks
        target=grid[y][x+1]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y, x+1)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            if randint(0, 1) == 0:
                return self.check_below(x,y, grid, counter+1)
            else:
                return self.check_above(x,y, grid, counter+1)

    def check_top_left(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention

        # Ceiling check
        if y <= 0:
            #* At the ceiling of the simulation, it can't go further up.
            #* This means that it should either go left or right.
            #* Since this particle originally intended to go upleft, it'll go left.
            return self.check_left(x,y, grid, counter+1)
        # Left edge check
        if x <= 0:
            #* At the left wall of the simulation, it can't go bottom left, top left, or left itself.
            #* This means that it should either go up or down, instead of trying the other side like standard particles.
            #* Since this particle originally intended to go upleft, it'll try to go up.
            return self.check_above(x,y, grid, counter+1)
        # Regular checks
        target=grid[y-1][x-1]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y-1, x-1)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            return self.check_above(x,y, grid, counter+1)
        
    def check_above(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention

        # Ceiling check
        if y <= 0:
            #* At the ceiling of the simulation, it can't go further up.
            #* This means that it should either go left or right.
            #* Since this particle originally intended to go straight up, it'll randomly go left or right.
            if randint(0, 1) == 0:
                return self.check_left(x,y, grid, counter+1)
            else:
                return self.check_right(x,y, grid, counter+1)
        # Regular checks
        target=grid[y-1][x]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y-1, x)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            if randint(0, 1) == 0:
                return self.check_left(x,y, grid, counter+1)
            else:
                return self.check_right(x,y, grid, counter+1)
    
    def check_top_right(self, x,y, grid, counter=0):
        #! Recursion prevention
        if counter >= 8:
            return False
        #! Recursion prevention

        # Ceiling check
        if y <= 0:
            #* At the ceiling of the simulation, it can't go further up.
            #* This means that it should either go left or right.
            #* Since this particle originally intended to go upright, it'll go right.
            return self.check_right(x,y, grid, counter+1)
        
        # Right edge check
        if x >= width-1:
            #* At the right wall of the simulation, it can't go bottom right, top right, or right itself.
            #* This means that it should either go up or down, instead of trying the other side like standard particles.
            #* Since this particle originally intended to go downright, it'll try to go down.
            return self.check_below(x,y, grid, counter+1)
        # Regular checks
        target=grid[y-1][x+1]
        if isinstance(target, (empty, LightGas)):
            self.move(grid, y,x, y-1, x+1)
            return True
        #TODO--- Gaseous interactions of varying densities
        else:
            return self.check_below(x,y, grid, counter+1)

    def check_movement(self, x,y, grid):
        r = random()
        ri = randint(0,2)
        # Upwards movements
        if r < 0.6:
            if ri == 0:
                return self.check_top_left(x,y, grid, 0)
            elif ri == 1:
                return self.check_above(x,y, grid, 0)
            else:
                return self.check_top_right(x,y, grid, 0)
        # Sideways movements
        elif r < 0.8:
            if randint(0,1) == 0:
                return self.check_left(x,y, grid, 0)
            else:
                return self.check_right(x,y, grid, 0)
        # Downwards movements
        elif r < 0.9:
            if ri == 0:
                return self.check_bottom_left(x,y, grid, 0)
            elif ri == 1:
                return self.check_below(x,y, grid, 0)
            else:
                return self.check_bottom_right(x,y, grid, 0)
        # Stay put
        else:
            return False



class Bouncy(Particle):
    def __init__(self, base_r, base_g, base_b, color_variance_red=20, color_variance_green=None, color_variance_blue=None):
        super().__init__(base_r, base_g, base_b, color_variance_red, color_variance_green, color_variance_blue)
        self.directions = ["topleft", "topright", "bottomleft", "bottomright"]
        self.current_direction = self.directions[randint(0,3)]
    def check_movement(self, x,y, grid):
        if self.current_direction == self.directions[0]:
            return self.check_top_left(x,y, grid)
        elif self.current_direction == self.directions[1]:
            return self.check_top_right(x,y, grid)
        elif self.current_direction == self.directions[2]:
            return self.check_bottom_left(x,y, grid)
        elif self.current_direction == self.directions[3]:
            return self.check_bottom_right(x,y, grid)
  
    def check_top_right(self, x,y, grid):
        # Topright Corner Bounce on grid
        if y <= 0 and x >= width-1:
            self.current_direction = self.directions[2]  # bottomleft
            return False
        # Corner Bounce on particles
        if y > 0 and x < width-1 and not isinstance(grid[y-1][x], empty) and not isinstance(grid[y][x+1], empty):
            self.current_direction = self.directions[2]  # bottomleft
            return False
        
        # Bounce on ceiling (horizontal surface - reverse vertical component)
        if y <= 0:
            self.current_direction = self.directions[3]  # bottomright
            return False
        
        # Bounce on right wall of grid (vertical surface - reverse horizontal component)
        if x >= width-1:
            self.current_direction = self.directions[0]  # topleft
            return False
        
        # Bounce on object above (horizontal surface) or to the right (vertical surface)
        if not isinstance(grid[y-1][x], empty):
            self.current_direction = self.directions[3]  # bottomright
            return False
        elif not isinstance(grid[y][x+1], empty):
            self.current_direction = self.directions[0]  # topleft
            return False
        # Move to empty spot
        else:
            self.move(grid, y, x, y-1, x+1)
            return True
        
    def check_top_left(self, x,y, grid):
        # Topleft Corner Bounce on grid
        if y <= 0 and x <= 0:
            self.current_direction = self.directions[3]  # bottomright
            return False
        # Corner Bounce on particles
        if y > 0 and x > 0 and not isinstance(grid[y-1][x], empty) and not isinstance(grid[y][x-1], empty):
            self.current_direction = self.directions[3]  # bottomright
            return False
        
        # Bounce on ceiling (horizontal surface - reverse vertical component)
        if y <= 0:
            self.current_direction = self.directions[2]  # bottomleft
            return False
        
        # Bounce on left wall of grid (vertical surface - reverse horizontal component)
        if x <= 0:
            self.current_direction = self.directions[1]  # topright
            return False
        
        # Bounce on object above (horizontal surface) or to the left (vertical surface)
        if not isinstance(grid[y-1][x], empty):
            self.current_direction = self.directions[2]  # bottomleft
            return False
        elif not isinstance(grid[y][x-1], empty):
            self.current_direction = self.directions[1]  # topright
            return False
        # Move to empty spot
        else:
            self.move(grid, y, x, y-1, x-1)
            return True
    
    def check_bottom_left(self, x,y, grid):
        # Bottomleft Corner Bounce on grid
        if y >= height-1 and x <= 0:
            self.current_direction = self.directions[1]  # topright
            return False
        # Corner Bounce on particles
        if y < height-1 and x > 0 and not isinstance(grid[y+1][x], empty) and not isinstance(grid[y][x-1], empty):
            self.current_direction = self.directions[1]  # topright
            return False
        
        # Bounce on floor (horizontal surface - reverse vertical component)
        if y >= height-1:
            self.current_direction = self.directions[0]  # topleft
            return False
        
        # Bounce on left wall of grid (vertical surface - reverse horizontal component)
        if x <= 0:
            self.current_direction = self.directions[3]  # bottomright
            return False
        
        # Bounce on object below (horizontal surface) or to the left (vertical surface)
        if not isinstance(grid[y+1][x], empty):
            self.current_direction = self.directions[0]  # topleft
            return False
        elif not isinstance(grid[y][x-1], empty):
            self.current_direction = self.directions[3]  # bottomright
            return False
        # Move to empty spot
        else:
            self.move(grid, y, x, y+1, x-1)
            return True
    
    def check_bottom_right(self, x,y, grid):
        # Bottomright Corner Bounce on grid
        if y >= height-1 and x >= width-1:
            self.current_direction = self.directions[0]  # topleft
            return False
        # Corner Bounce on particles
        if y < height-1 and x < width-1 and not isinstance(grid[y+1][x], empty) and not isinstance(grid[y][x+1], empty):
            self.current_direction = self.directions[0]  # topleft
            return False
        
        # Bounce on floor (horizontal surface - reverse vertical component)
        if y >= height-1:
            self.current_direction = self.directions[1]  # topright
            return False
        
        # Bounce on right wall of grid (vertical surface - reverse horizontal component)
        if x >= width-1:
            self.current_direction = self.directions[2]  # bottomleft
            return False
        
        # Bounce on object below (horizontal surface) or to the right (vertical surface)
        if not isinstance(grid[y+1][x], empty):
            self.current_direction = self.directions[1]  # topright
            return False
        elif not isinstance(grid[y][x+1], empty):
            self.current_direction = self.directions[2]  # bottomleft
            return False
        # Move to empty spot
        else:
            self.move(grid, y, x, y+1, x+1)
            return True



# Granular particles
class sand(Granular):
    color = (194, 178, 128)  # Sandy beige color
    color_variance = (20,)
    def __init__(self):
        self.conductivity = 0.015
        self.decay_factor = 0.002
        # temperature defaults to ambient_temperature +/- 2.5 (use fallback 20 if not defined yet)
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)
        # color variance: default (same as Particle default)
        self.color_variance = (20,)
        super().__init__(self.color[0], self.color[1], self.color[2])

class dirt(Granular):
    color = (139, 115, 85)  # Earthy brown, lighter and less saturated than mud
    color_variance = (20,)
    def __init__(self):
        self.conductivity = 0.02
        self.decay_factor = 0.003
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)
        # color variance: default
        self.color_variance = (20,)
        super().__init__(self.color[0], self.color[1], self.color[2])

# Liquid particles  
class water(Liquid):
    color = (64, 164, 223)  # Blue color
    color_variance = (20,)
    def __init__(self):
        self.conductivity = 0.03
        self.decay_factor = 0.005
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)

        self.evap_temp = 100
        self.evap_to = steam

        self.solidify_temp = 0
        self.solidify_to = ice
        self.solidify_color = colorer(ice.color[0], ice.color[1], ice.color[2], ice.color_variance[0] if hasattr(ice, 'color_variance') else 20)

        super().__init__(self.color[0], self.color[1], self.color[2])

class lava(Liquid):
    color = (255, 80, 0)
    color_variance = (45,)
    def __init__(self):
        self.conductivity = 0.08
        self.decay_factor = 0.0035
        # Base 1125 +/-125 variation
        self.temperature = 1125 + (random() * 250.0 - 125.0)

        self.solidify_temp = 200 # Celsius
        self.solidify_to = basalt
        self.solidify_color = colorer(basalt.color[0], basalt.color[1], basalt.color[2], basalt.color_variance[0] if hasattr(basalt, 'color_variance') else 20)
        
        self.viscosity = 2 # Lava moves slower
        self.viscosity_timer = 0

        super().__init__(self.color[0], self.color[1], self.color[2], *self.color_variance)

# Straight falling particles
class stone(StraightFalling):
    color = (68, 68, 68)  # Gray with less variance
    color_variance = (10,)
    def __init__(self):
        self.conductivity = 0.03
        self.decay_factor = 0.002
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)
        super().__init__(self.color[0], self.color[1], self.color[2], *self.color_variance)

class mud(StraightFalling):
    color = (101, 67, 33)   # Dark brown color
    color_variance = (20,)
    def __init__(self):
        self.conductivity = 0.02
        self.decay_factor = 0.003
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)
        self.lifetime = randint(50,100)
        self.max_lifetime = self.lifetime
        super().__init__(self.color[0], self.color[1], self.color[2])

class wet_sand(StraightFalling):
    color = (160, 140, 100)  # Darker sandy beige color
    color_variance = (20,)
    def __init__(self):
        self.conductivity = 0.02
        self.decay_factor = 0.003
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)
        self.lifetime = randint(50,100)
        self.max_lifetime = self.lifetime
        super().__init__(self.color[0], self.color[1], self.color[2])

class ice(StraightFalling):
    color = (180, 220, 255)  # Pale blue-white for ice
    color_variance = (10,)
    def __init__(self):
        # Ice is a poor conductor compared to metals, but better than air
        self.conductivity = 0.015
        # Decays slowly toward ambient temperature (melts slowly)
        self.decay_factor = 0.001
        # Ice is cold by default, well below room temperature
        self.temperature = -10.0
        # Melts at 0°C, turns into water
        self.melt_temp = 0
        self.melt_to = water
        self.melt_color = colorer(water.color[0], water.color[1], water.color[2], water.color_variance[0] if hasattr(water, 'color_variance') else 20)
        super().__init__(self.color[0], self.color[1], self.color[2], *self.color_variance)

# Light Gaseous particles
class steam(LightGas):
    color = (200, 200, 220)  # Light grayish color
    color_variance = (15,)
    def __init__(self):
        # self.conductivity = 0.05
        # self.decay_factor = 0.015
        self.conductivity = 0.004
        self.decay_factor = 0.025
        self.condense_to = water
        self.condense_temp = 100

        self.condensing_framecount = 180 + randint(0,40)
        self.condense_timer = 0

        # Temperature variation across 100..275 (centered variation)
        self.temperature = 187.5 + (random() * 175.0 - 87.5)
        super().__init__(self.color[0], self.color[1], self.color[2], *self.color_variance)

class fire(LightGas):
    color = (255, 150, 0)  # Light grayish color
    color_variance = (15,)
    def __init__(self):
        self.conductivity = 0.05
        self.decay_factor = 0.015
        self.temperature = 187.5 + (random() * 175.0 - 87.5)
        self.lifetime = randint(30, 60)  # Lifetime in frames
        self.max_lifetime = self.lifetime
        super().__init__(self.color[0], self.color[1], self.color[2], *self.color_variance)

# Static particles
class empty(Static):
    color = (0, 0, 0)  # Black with no variance
    color_variance = (0,)
    def __init__(self):
        self.conductivity = 0.01
        self.decay_factor = 0.035
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)
        super().__init__(self.color[0], self.color[1], self.color[2], *self.color_variance)

class basalt(Static):
    color = (76, 74, 74)  # Dark blue with minimal variance
    color_variance = (35,)
    def __init__(self):
        self.conductivity = 0.03
        self.decay_factor = 0.002
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)

        self.melt_temp = 1000 # Celsius
        self.melt_to = lava
        self.melt_color = colorer(lava.color[0], lava.color[1], lava.color[2], lava.color_variance[0] if hasattr(lava, 'color_variance') else 20)

        # color variance: basalt has larger variance
        super().__init__(self.color[0], self.color[1], self.color[2], *self.color_variance)


# Bouncy particles
class bouncy_ball(Bouncy):
    color = (255, 0, 255)  # Bright magenta color
    color_variance = (20,)
    def __init__(self):
        self.viscosity_timer = 0
        self.viscosity =  5
        self.temperature = globals().get('ambient_temperature', 20) + (random() * 5.0 - 2.5)
        super().__init__(self.color[0], self.color[1], self.color[2])

width, height=150,100
grid = [[empty() for _ in range(width)] for _ in range(height)]


cell_size=10
sidebar_width = 150
selected_particle = sand  # Default selection
pygame.init()
screen = pygame.display.set_mode((width * cell_size + sidebar_width, height * cell_size))
clock = pygame.time.Clock()
running = True
paused = False

def draw_grid():
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            pygame.draw.rect(
                screen,
                cell.color,
                (x * cell_size, y * cell_size, cell_size, cell_size)
            )
    pygame.display.flip()

def get_all_subclasses(cls):
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_all_subclasses(subclass))
    return subclasses

def get_particle_colors():
    color_dict = {}
    for subclass in get_all_subclasses(Particle):
        # only include "end" classes, not base ones like Granular
        if not subclass.__subclasses__():
            instance = subclass()  # create one so we can read its base color
            color_dict[subclass] = instance.base_color
            # Store the variance as a tuple (red, green, blue)
            # Try to get the variance values from the constructor args or attributes
            # Prefer the new unified `color_variance` attribute when present
            red = getattr(instance, 'color_variance_red', None)
            green = getattr(instance, 'color_variance_green', None)
            blue = getattr(instance, 'color_variance_blue', None)
            if hasattr(instance, 'color_variance'):
                cv = instance.color_variance
                if isinstance(cv, (list, tuple)):
                    if len(cv) == 1:
                        red = cv[0]
                        green = cv[0]
                        blue = cv[0]
                    elif len(cv) == 3:
                        red, green, blue = cv
                    else:
                        # Fallback: use first value for all channels
                        red = cv[0]
                        green = red
                        blue = red
                else:
                    # single numeric value
                    red = cv
                    green = cv
                    blue = cv
            # Final fallbacks to maintain original behavior
            if red is None:
                red = 20
            if green is None:
                green = red
            if blue is None:
                blue = red
            color_dict[f"{subclass.__name__}_var"] = (red, green, blue)
    return color_dict

PARTICLE_COLORS = get_particle_colors()




particle_list = [cls for cls in get_all_subclasses(Particle)
                 if not cls.__subclasses__()]

for y in range(0,47):
    for x in range(0,50):
        grid[y][x] = water()

def handle_particle_specials(x, y, grid):
    target=grid[y][x]

    #! Handle condensation
    #! 3 cells need to surround the cell if that cell wants to condense, lowers on lower temperatures. 
    if hasattr(target, 'condense_to'):
        if target.temperature <= target.condense_temp:
            target.condense_timer += 1
            if target.condense_timer >= target.condensing_framecount:
                # Edge checks for grid boundaries
                orthogonal_neighbours = 0
                steam_neighbours = []
                for yi in range(-1,2):
                    if orthogonal_neighbours == 3:
                            break
                    for xi in range(-1,2):
                        if orthogonal_neighbours == 3:
                            break
                        
                        # Wall checks
                        if y+yi < 0 or y+yi >= height or x+xi < 0 or x+xi >= width:
                            continue
                        if yi != xi:
                            if isinstance(grid[y+yi][x+xi], steam): 
                                orthogonal_neighbours+=1
                                steam_neighbours.append((y+yi, x+xi))

                if orthogonal_neighbours == 3:
                    neighbour_1 = grid[steam_neighbours[0][0]][steam_neighbours[0][1]]
                    neighbour_2 = grid[steam_neighbours[1][0]][steam_neighbours[1][1]]
                    neighbour_3 = grid[steam_neighbours[2][0]][steam_neighbours[2][1]]
                    grid[y][x] = target.condense_to()
                    grid[y][x].temperature = target.temperature
                    grid[steam_neighbours[0][0]][steam_neighbours[0][1]] = empty()
                    grid[steam_neighbours[0][0]][steam_neighbours[0][1]].temperature = neighbour_1.temperature
                    grid[steam_neighbours[1][0]][steam_neighbours[1][1]] = empty()
                    grid[steam_neighbours[1][0]][steam_neighbours[1][1]].temperature = neighbour_2.temperature
                    grid[steam_neighbours[2][0]][steam_neighbours[2][1]] = empty()
                    grid[steam_neighbours[2][0]][steam_neighbours[2][1]].temperature = neighbour_3.temperature

    
    #! Fire>Dissapear
    if isinstance(grid[y][x], fire):
        grid[y][x].lifetime -= 1
        if grid[y][x].lifetime <= 0:
            grid[y][x] = empty()

    #! Handle solidification
    #! Color transitions will apply.
    if hasattr(grid[y][x], 'solidify_to'):
        p = grid[y][x]

        # use the particle's original spawned color for the transition
        original_hsv = rgb_to_hsv(p.spawn_color[0] / 255.0,
                                  p.spawn_color[1] / 255.0,
                                  p.spawn_color[2] / 255.0)
        new_hsv = rgb_to_hsv(p.solidify_color[0] / 255.0,
                                p.solidify_color[1] / 255.0,
                                p.solidify_color[2] / 255.0)

        # fixed temp range: hot->cold
        # Use the correct temperature range for solidifying (from original temp down to solidify_temp)
        if not hasattr(p, 'original_temp'):
            p.original_temp = p.temperature  # store the original temp at spawn
        temp_range = max(1.0, p.original_temp - p.solidify_temp)
        # Progress should be 0 when hot, 1 when cold (so invert)
        temp_progress = 1.0 - ((p.temperature - p.solidify_temp) / temp_range)
        temp_progress = max(0.0, min(1.0, temp_progress))

        # interpolate from the original (spawn) HSV -> basalt HSV
        new_h = original_hsv[0] + (new_hsv[0] - original_hsv[0]) * temp_progress
        new_s = original_hsv[1] + (new_hsv[1] - original_hsv[1]) * temp_progress
        new_v = original_hsv[2] + (new_hsv[2] - original_hsv[2]) * temp_progress

        new_rgb = hsv_to_rgb(new_h, new_s, new_v)
        # assign ints and clamp
        p.color = (int(max(0, min(255, new_rgb[0] * 255))),
                   int(max(0, min(255, new_rgb[1] * 255))),
                   int(max(0, min(255, new_rgb[2] * 255))))

        if p.temperature <= p.solidify_temp:
            grid[y][x] = p.solidify_to()
            grid[y][x].temperature = p.temperature
            grid[y][x].color = p.solidify_color
    

    #! Handle melting
    #! Color transitions will apply
    if hasattr(grid[y][x], 'melt_to'):
        p = grid[y][x]

        # use the particle's original spawned color for the transition
        original_hsv = rgb_to_hsv(p.spawn_color[0] / 255.0,
                                  p.spawn_color[1] / 255.0,
                                  p.spawn_color[2] / 255.0)
        new_hsv = rgb_to_hsv(p.melt_color[0] / 255.0,
                                p.melt_color[1] / 255.0,
                                p.melt_color[2] / 255.0)

        if not hasattr(p, 'original_temp'):
            p.original_temp = p.temperature  # store the original temp at spawn
        temp_range = max(1.0, p.melt_temp - p.original_temp)
        # Progress should be 0 when cold (original), 1 when hot (melted)
        temp_progress = (p.temperature - p.original_temp) / temp_range
        temp_progress = max(0.0, min(1.0, temp_progress))

        # interpolate from the original (spawn) HSV -> basalt HSV
        new_h = original_hsv[0] + (new_hsv[0] - original_hsv[0]) * temp_progress
        new_s = original_hsv[1] + (new_hsv[1] - original_hsv[1]) * temp_progress
        new_v = original_hsv[2] + (new_hsv[2] - original_hsv[2]) * temp_progress

        new_rgb = hsv_to_rgb(new_h, new_s, new_v)
        # assign ints and clamp
        p.color = (int(max(0, min(255, new_rgb[0] * 255))),
                   int(max(0, min(255, new_rgb[1] * 255))),
                   int(max(0, min(255, new_rgb[2] * 255))))

        if p.temperature >= p.melt_temp:
            grid[y][x] = p.melt_to()
            grid[y][x].temperature = p.temperature
            grid[y][x].color = p.melt_color

    #! Handle evaporation
    if hasattr(target, 'evap_to'):
        if target.temperature >= target.evap_temp:
            grid[y][x] = target.evap_to()
            grid[y][x].temperature = target.temperature

    #! Mud>Dirt
    if isinstance(grid[y][x], mud):
        p = grid[y][x]
        p.lifetime -= 1
        red_drying_increment = ((PARTICLE_COLORS[dirt][0] - PARTICLE_COLORS[mud][0])/p.max_lifetime)
        green_drying_increment = ((PARTICLE_COLORS[dirt][1] - PARTICLE_COLORS[mud][1])/p.max_lifetime)
        blue_drying_increment = ((PARTICLE_COLORS[dirt][2] - PARTICLE_COLORS[mud][2])/p.max_lifetime)
        new_r = max(0, min(255, p.color[0] + red_drying_increment))
        new_g = max(0, min(255, p.color[1] + green_drying_increment))
        new_b = max(0, min(255, p.color[2] + blue_drying_increment))
        p.color = (new_r, new_g, new_b)

        if p.lifetime <= 0:
            grid[y][x] = dirt()
    
    if isinstance(grid[y][x], wet_sand):
        p = grid[y][x]
        p.lifetime -= 1
        red_drying_increment = ((PARTICLE_COLORS[sand][0] - PARTICLE_COLORS[wet_sand][0])/p.max_lifetime)
        green_drying_increment = ((PARTICLE_COLORS[sand][1] - PARTICLE_COLORS[wet_sand][1])/p.max_lifetime)
        blue_drying_increment = ((PARTICLE_COLORS[sand][2] - PARTICLE_COLORS[wet_sand][2])/p.max_lifetime)
        new_r = max(0, min(255, p.color[0] + red_drying_increment))
        new_g = max(0, min(255, p.color[1] + green_drying_increment))
        new_b = max(0, min(255, p.color[2] + blue_drying_increment))
        p.color = (new_r, new_g, new_b)

        if p.lifetime <= 0:
            grid[y][x] = sand()

def draw_sidebar():
    sidebar_x = width * cell_size
    particle_types = particle_list

    # Draw sidebar background
    pygame.draw.rect(screen, (50, 50, 50), (sidebar_x, 0, sidebar_width, height * cell_size))
    
    # Draw particle options
    font = pygame.font.SysFont(None, 24)
    font_small = pygame.font.SysFont(None, 18)
    for i, particle_type in enumerate(particle_types):
        y_pos = i * 60 + 10

        # Use definitive color instead of creating sample particle
        color = PARTICLE_COLORS[particle_type]

        # Draw colored rectangle
        box_rect = pygame.Rect(sidebar_x + 10, y_pos, 40, 40)
        pygame.draw.rect(screen, color, box_rect)

        # Highlight selected particle
        if particle_type == selected_particle:
            pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)

        # Draw the particle name inside the color box
        # Format class name to something user-friendly (replace underscores, title case)
        display_name = particle_type.__name__.replace('_', ' ').title()

        # Choose text color based on luminance for contrast
        r, g, b = color
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = (0, 0, 0) if luminance > 160 else (255, 255, 255)

        # Trim text with ellipsis if it doesn't fit the box using font_small
        txt = display_name
        name_surf = font_small.render(txt, True, text_color)
        # reduce until it fits (allow a 4px padding)
        if name_surf.get_width() > box_rect.width - 4:
            # progressively trim and add ellipsis
            while name_surf.get_width() > box_rect.width - 6 and len(txt) > 1:
                txt = txt[:-1]
                name_surf = font_small.render(txt + '...', True, text_color)
            if name_surf.get_width() <= box_rect.width - 6:
                name_surf = font_small.render(txt + '...', True, text_color)

        # Center the text inside the color box
        name_rect = name_surf.get_rect(center=box_rect.center)
        screen.blit(name_surf, name_rect)
    # Draw temperature input box above the pause button
    global paused, temperature_input_active, temperature_input_text
    input_box_rect = pygame.Rect(sidebar_x + 10, height * cell_size - 110, sidebar_width - 20, 40)
    font = pygame.font.SysFont(None, 24)
    # label
    label_surf = font.render("Ambient Temp:", True, (255, 255, 255))
    screen.blit(label_surf, (input_box_rect.x, input_box_rect.y - 20))

    # input box background
    pygame.draw.rect(screen, (30, 30, 30), input_box_rect)
    # highlight if active
    if temperature_input_active:
        pygame.draw.rect(screen, (200, 200, 200), input_box_rect, 2)
    else:
        pygame.draw.rect(screen, (100, 100, 100), input_box_rect, 2)

    # render current text
    text_surf = font.render(temperature_input_text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(midleft=(input_box_rect.x + 6, input_box_rect.centery))
    screen.blit(text_surf, text_rect)

    # Draw pause button
    pause_button_rect = pygame.Rect(sidebar_x + 10, height * cell_size - 60, sidebar_width - 20, 40)
    pygame.draw.rect(screen, (100, 100, 100), pause_button_rect)
    font_big = pygame.font.SysFont(None, 32)
    pause_text = "Pause" if not paused else "Resume"
    text_surface = font_big.render(pause_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=pause_button_rect.center)
    screen.blit(text_surface, text_rect)

    # Handle pause button click (kept here so it responds during draw)
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_pressed[0] and pause_button_rect.collidepoint(mouse_x, mouse_y):
        paused = not paused
        pygame.time.wait(200)  # Debounce click

frame_delay = 0
simulation_speed = 1
ambient_temperature = -20
temperature_decay_factor = 0.005
# UI state for the temperature input box in the sidebar
temperature_input_active = False
temperature_input_text = str(ambient_temperature)

def update_frame():
    # First pass: Movement
    for y in range(height-1, -1, -1):  # Bottom to top
        for x in range(width):
            cell = grid[y][x]
           
            # Check if the cell has a check_below method and hasn't moved
            if hasattr(cell, 'check_movement') and hasattr(cell, 'has_moved') and not cell.has_moved:
                
                # Slower moving items all fall under the attribute 'viscosity'
                if hasattr(cell, 'viscosity') and not hasattr(cell, 'viscosity_timer'):
                    cell.viscosity_timer = 0
                if hasattr(cell, 'viscosity_timer') and not hasattr(cell, 'viscosity'):
                    raise LookupError("Viscosity timer found without matching visocisity attribute")
                
                if hasattr(cell, 'viscosity'):
                    cell.viscosity_timer += 1
                    if cell.viscosity_timer <= cell.viscosity:
                        continue
                    if cell.viscosity_timer > cell.viscosity:
                        cell.viscosity_timer = 0
                if cell.check_movement(x, y, grid):
                    cell.has_moved = True
    
    # Second pass: Check for interactions
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]

            handle_particle_specials(x, y, grid)
            #^ Example: Aging steam particles eventually turn into water

            if not isinstance(cell, empty):
                check_interactions(x, y, grid)
    
    # Third pass: Reset has_moved flag for next frame
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            if hasattr(cell, 'has_moved'):
                cell.has_moved = False
    # Delay frame
    pygame.time.delay(frame_delay)

    # Fourth pass: Thermal dynamics
    for y in range(height):
        for x in range(width):
            cell=grid[y][x]
            conduction = 0
            ambient_decay = cell.temperature + (ambient_temperature - cell.temperature) * cell.decay_factor

            if y > 0:
                upper = grid[y-1][x]
                conduction += (upper.temperature - cell.temperature) * ((upper.conductivity + cell.conductivity)/2)
            if y < height-1:
                lower = grid[y+1][x]
                conduction += (lower.temperature - cell.temperature) * ((lower.conductivity + cell.conductivity)/2)
            if x > 0:
                left = grid[y][x-1]
                conduction += (left.temperature - cell.temperature) * ((left.conductivity + cell.conductivity)/2)
            if x < width-1:
                right = grid[y][x+1]
                conduction += (right.temperature - cell.temperature) * ((right.conductivity + cell.conductivity)/2)
            cell.new_temperature = ambient_decay + conduction
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            grid[y][x].temperature = cell.new_temperature
            grid[y][x].new_temperature = 0

def check_interactions(x, y, grid):
    """Check for interactions with adjacent particles"""
    current_particle = grid[y][x]

    directions = [
        (0, 1),   # below
        (0, -1),  # above
        (1, 0),   # right
        (-1, 0),  # left
        (1, 1),   # bottom-right
        (-1, 1),  # bottom-left
        (1, -1),  # top-right
        (-1, -1)  # top-left
    ]
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        
        # Bounds checking
        if 0 <= new_x < width and 0 <= new_y < height:
            neighbor_particle = grid[new_y][new_x]
            
            # Check for interaction
            interaction_func = get_interaction(current_particle, neighbor_particle)
            if interaction_func:
                interaction_func(new_x, new_y, x, y, grid)
                return  # Only process one interaction per particle per frame

def sa_wa_ws(new_x, new_y, old_x, old_y, grid):
        grid[new_y][new_x] = wet_sand()
        grid[old_y][old_x] = empty()

def di_wa_mu(new_x, new_y, old_x, old_y, grid):
        grid[new_y][new_x] = mud()
        grid[old_y][old_x] = empty()

# def wa_la_ba(new_x, new_y, old_x, old_y, grid):
#         grid[new_y][new_x] = basalt()
#         r=random()
#         if r > .9:
#             print(r)
#             grid[old_y][old_x] = steam()

def la_st_la(new_x, new_y, old_x, old_y, grid):
        grid[new_y][new_x] = lava()
        grid[old_y][old_x] = lava()

INTERACTIONS = {
    "water+sand": sa_wa_ws, # Wet Sand
    "sand+water": sa_wa_ws, #
    "dirt+water": di_wa_mu, # Mud
    "water+dirt": di_wa_mu, #
    # "lava+water": wa_la_ba, # Basalt
    # "water+lava": wa_la_ba, #
    "lava+stone": la_st_la, # Lava-fy
    "stone+lava": la_st_la, #
}

def get_interaction(particle1, particle2):
    key = f"{particle1.__class__.__name__}+{particle2.__class__.__name__}"
    return INTERACTIONS.get(key)
    


def event_handler():
    global selected_particle, running
    global temperature_input_active, temperature_input_text, ambient_temperature

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_EQUALS:  # + key
        #         simulation_speed = min(5, simulation_speed + 0.5)
        #     elif event.key == pygame.K_MINUS:  # - key
        #         simulation_speed = max(0.1, simulation_speed - 0.5)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < width * cell_size:  # Click in grid area
                grid_x = mouse_x // cell_size
                grid_y = mouse_y // cell_size
                if grid_x < width and grid_y < height:
                    if event.button == 1:  # Left click
                        grid[grid_y][grid_x] = selected_particle()
                    elif event.button == 3:  # Right click
                        grid[grid_y][grid_x] = empty()
            else:  # Click in sidebar
                sidebar_x = width * cell_size
                # check if clicked the temperature input box
                input_box_rect = pygame.Rect(sidebar_x + 10, height * cell_size - 110, sidebar_width - 20, 40)
                pause_button_rect = pygame.Rect(sidebar_x + 10, height * cell_size - 60, sidebar_width - 20, 40)

                if input_box_rect.collidepoint(mouse_x, mouse_y):
                    # focus the input box for typing
                    temperature_input_active = True
                elif pause_button_rect.collidepoint(mouse_x, mouse_y):
                    # leave to the draw_sidebar click handler (it toggles paused)
                    temperature_input_active = False
                else:
                    # clicking the particle selection area should defocus input
                    temperature_input_active = False
                    particle_types = particle_list
                    clicked_index = (mouse_y - 10) // 60
                    if 0 <= clicked_index < len(particle_types):
                        selected_particle = particle_types[clicked_index]
                        # small debounce so accidental clicks don't re-open input
                        pygame.time.wait(80)
        elif event.type == pygame.KEYDOWN:
            # Keyboard events only affect the temperature input when it's active
            if temperature_input_active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # try to parse and apply
                    try:
                        new_temp = float(temperature_input_text)
                        ambient_temperature = new_temp
                        # normalize displayed text
                        temperature_input_text = str(ambient_temperature)
                    except Exception:
                        # invalid input: reset to current room temperature
                        temperature_input_text = str(ambient_temperature)
                    temperature_input_active = False
                elif event.key == pygame.K_ESCAPE:
                    # cancel editing
                    temperature_input_text = str(ambient_temperature)
                    temperature_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    temperature_input_text = temperature_input_text[:-1]
                else:
                    # only accept digits, minus and dot
                    ch = event.unicode
                    if ch and ch in '0123456789.-':
                        temperature_input_text += ch

def update_grid():
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0] or mouse_buttons[2]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < width * cell_size:  # Only grid area
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size
            if 0 <= grid_x < width and 0 <= grid_y < height:
                if mouse_buttons[0]:
                    grid[grid_y][grid_x] = selected_particle()
                elif mouse_buttons[2]:
                    grid[grid_y][grid_x] = empty()


print(particle_list)
print(len(particle_list))
while running:
    event_handler()
    update_grid()
    if paused == False:
        update_frame()
    draw_grid()
    draw_sidebar()
    clock.tick(60)
