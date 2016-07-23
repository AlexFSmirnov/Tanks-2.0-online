import pygame
from pygame import *


# This class allows you to create a special resizable pygame window.
# The main surface will remain undistorted, and the part of the window,
# that is not used, will be filled.
#
# All constructor variables are explained in the readme, but if you want 
# to understand the code, this description of the variables may help you:
#
# display_surface - the surface, that will be displayed on the screen
# background_surface - the surface with the gap filling
# main_surface - the surface, that you don't want to be distorted
# 
# d_w, d_h (you can see these in some functions) - the size (width and height)
#                                                       of the displayed window
# m_w, m_h - the size of the main_surface


class ResizableWindow:
    def __init__(self,
                 initial_size,
                 main_size,
                 gap_fill_type  = "solid_color",
                 gap_fill_color = (0, 0, 0),
                 gap_steps      = 100,
                 draw_lines     = True,
                 lines_color    = (100, 100, 100),
                 smoothscale    = True):
        
        self.display_surface    = pygame.Surface(initial_size)
        self.background_surface = pygame.Surface(initial_size)
        self.main_surface       = pygame.Surface(main_size)
        self.screen = display.set_mode(initial_size, 
                                               HWSURFACE|DOUBLEBUF|RESIZABLE)        
        
        self.main_size = main_size
        self.current_size = initial_size
        
        self.draw_lines = draw_lines
        self.lines_color = lines_color
        self.smoothscale = smoothscale
        
        self.gaps_pos = ""
        self.updateGapsPos(initial_size)
        
        # Creating the gap fill.  
        self.gap_fill = pygame.Surface((gap_steps, gap_steps))
        if gap_fill_type == "solid_color":
            self.gap_fill.fill(gap_fill_color)
        elif gap_fill_type == "gradient_up":
            for y in range(gap_steps):
                for x in range(gap_steps):
                    self.gap_fill.set_at((x, y), gap_fill_color)
                gap_fill_color = [min(i + 1, 255) for i in gap_fill_color]
        elif gap_fill_type == "gradient_down":
            for y in range(gap_steps):
                for x in range(gap_steps):
                    self.gap_fill.set_at((x, y), gap_fill_color)
                gap_fill_color = [max(i - 1, 0) for i in gap_fill_color] 
    
    def updateMainSurface(self, new_main_surface):
        self.main_surface = transform.scale(new_main_surface, self.main_size)  
    
    def blitMainSurface(self):
        if self.smoothscale:
            scaled_main = transform.smoothscale(self.main_surface, 
                                                self.main_scale)
        else:
            scaled_main = transform.scale(self.main_surface, self.main_scale)
        self.display_surface.blit(scaled_main, self.main_pos)  
    
    def getMousePos(self):  # Sort of magic here.
        x, y = mouse.get_pos()
        d_w, d_h = self.display_surface.get_size()
        m_w, m_h = self.main_size

        if self.gaps_pos == "sides":
            s_w, s_h = d_h / m_h * m_w, d_h  # The size of the scales main surf
            x = (x - (d_w - s_w) // 2) * m_w // s_w  
            y = y * m_h // s_h
        elif self.gaps_pos == "above and below":
            s_w, s_h = d_w, d_w / m_w * m_h
            x = x * m_w // s_w
            y = (y - (d_h - s_h) // 2) * m_h // s_h 

        return (x, y)
        
    def updateGapsPos(self, new_size):
        d_w, d_h = new_size
        m_w, m_h = self.main_size
        if d_h / (d_w / m_w) >= m_h:
            self.gaps_pos = "above and below"
        else:
            self.gaps_pos = "sides"
        
    def updateBackgroundSurface(self, new_size):
        d_w, d_h = new_size
        m_w, m_h = self.main_size
        self.background_surface = Surface(new_size)
        gap = self.gap_fill
        
        if self.gaps_pos == "above and below":
            gap_size = (d_w, round((d_h - d_w / m_w * m_h) / 2) + 1)
            gap_top = transform.scale(transform.rotate(gap, 180), gap_size)
            gap_bottom = transform.scale(transform.rotate(gap, 0), gap_size)
            
            self.background_surface.blit(gap_top, (0, 0))
            self.background_surface.blit(gap_bottom, (0, d_h - gap_size[1]))
            
            if self.draw_lines:
                # -1 here - sort of a duct tape. It works, and idk why :P
                draw.line(self.background_surface, self.lines_color,
                          (0, gap_size[1] - 1), (d_w, gap_size[1] - 1), 6)
                draw.line(self.background_surface, self.lines_color,
                                  (0, d_h - gap_size[1] - 1), 
                                  (d_w, d_h - gap_size[1] - 1), 6)
        elif self.gaps_pos == "sides":
            gap_size = (round((d_w - d_h / m_h * m_w) / 2) + 1, d_h)
            gap_left = transform.scale(transform.rotate(gap, -90), gap_size)
            gap_right = transform.scale(transform.rotate(gap, 90), gap_size)
            
            self.background_surface.blit(gap_left, (0, 0))
            self.background_surface.blit(gap_right, (d_w - gap_size[0], 0))
            
            if self.draw_lines:
                # -1 here - just the same duct tape.
                draw.line(self.background_surface, self.lines_color,
                          (gap_size[0] - 1, 0), (gap_size[0] - 1, d_h), 6)
                draw.line(self.background_surface, self.lines_color,
                          (d_w - gap_size[0] - 1, 0), 
                          (d_w - gap_size[0] - 1, d_h), 6)  
        self.update()
    
    def updateDisplaySurface(self, new_size):
        d_w, d_h = new_size
        m_w, m_h = self.main_size
        self.display_surface = Surface(new_size)
        
        if self.gaps_pos == "above and below":
            self.main_scale = (d_w, round(d_w / m_w * m_h))
            self.main_pos   = (0, round((d_h - self.main_scale[1]) / 2))
        elif self.gaps_pos == "sides":
            self.main_scale = (round(d_h / m_h * m_w), d_h)
            self.main_pos   = (round((d_w - self.main_scale[0]) / 2), 0)
        self.display_surface.blit(self.background_surface, (0, 0))
        self.blitMainSurface()
    
    def updateScreen(self, new_size):
        self.screen = display.set_mode(new_size, 
                                       HWSURFACE|DOUBLEBUF|RESIZABLE)
        
    def updateSize(self, new_size):
        self.updateGapsPos(new_size)
        self.updateBackgroundSurface(new_size)
        self.updateDisplaySurface(new_size)  
        self.updateScreen(new_size)
    
    def update(self):
        self.updateDisplaySurface(self.display_surface.get_size())  
        self.screen.blit(self.display_surface, (0, 0))
        pygame.display.update()
