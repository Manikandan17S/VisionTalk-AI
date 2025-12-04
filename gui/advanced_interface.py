import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import random
import threading
import time as time_module

# ==================== OPTIMIZED 3D JARVIS CORE ====================
class JarvisHolographicCore:
    def __init__(self, width=1600, height=900):
        """Optimized 3D holographic JARVIS core"""
        pygame.init()
        self.display = (width, height)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("JARVIS - Holographic AI Interface")
        
        # OpenGL setup
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        
        # Perspective
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -8)
        
        # State
        self.rotation = 0
        self.time = 0
        self.particles = []
        self.state = "standby"
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame_count = 0
        
        # Create particles
        self.create_particles()
    
    def create_particles(self):
        """Create particles"""
        self.particles = []
        for _ in range(50): 
            angle = random.uniform(0, 2 * math.pi)
            elevation = random.uniform(0, math.pi)
            
            p = {
                'x': 0, 'y': 0, 'z': 0,
                'vx': math.cos(angle) * math.cos(elevation) * 0.05,
                'vy': math.sin(elevation) * 0.05,
                'vz': math.sin(angle) * math.cos(elevation) * 0.05,
                'life': 1.0,
                'size': random.uniform(2, 5)
            }
            self.particles.append(p)
    
    def draw_sphere_wireframe(self, radius, color):
        """Draw wireframe sphere (optimized)"""
        glColor4f(color[0], color[1], color[2], 0.8)
        
       
        for i in range(0, 180, 36): 
            glBegin(GL_LINE_LOOP)
            for j in range(0, 360, 36): 
                lat = math.radians(i)
                lon = math.radians(j)
                x = radius * math.sin(lat) * math.cos(lon)
                y = radius * math.cos(lat)
                z = radius * math.sin(lat) * math.sin(lon)
                glVertex3f(x, y, z)
            glEnd()
        
        for j in range(0, 360, 36):  
            glBegin(GL_LINE_LOOP)
            for i in range(0, 180, 36):  
                lat = math.radians(i)
                lon = math.radians(j)
                x = radius * math.sin(lat) * math.cos(lon)
                y = radius * math.cos(lat)
                z = radius * math.sin(lat) * math.sin(lon)
                glVertex3f(x, y, z)
            glEnd()
    
    def draw_rings(self, color):
        """Draw rotating rings (optimized)"""
        glLineWidth(2.0)
        
        # Ring 1
        glPushMatrix()
        glRotatef(self.time * 50, 0, 1, 0)
        glColor4f(color[0], color[1], color[2], 0.6)
        glBegin(GL_LINE_LOOP)
        for i in range(0, 100, 5):  
            angle = (i / 100) * 2 * math.pi
            x = math.cos(angle) * 2.2
            z = math.sin(angle) * 2.2
            glVertex3f(x, 0, z)
        glEnd()
        glPopMatrix()
        
        # Ring 2 (optimized)
        glPushMatrix()
        glRotatef(self.time * 40, 1, 0, 1)
        glColor4f(color[0], color[1], color[2], 0.5)
        glBegin(GL_LINE_LOOP)
        for i in range(0, 100, 5):  
            angle = (i / 100) * 2 * math.pi
            x = math.cos(angle) * 2.5
            y = math.sin(angle) * 0.3
            glVertex3f(x, y, 0)
        glEnd()
        glPopMatrix()
    
    def draw_particles(self, color):
        """Draw energy particles"""
        glPointSize(4.0)
        glBegin(GL_POINTS)
        
        for p in self.particles:
            glColor4f(color[0], color[1], color[2], p['life'])
            glVertex3f(p['x'], p['y'], p['z'])
        
        glEnd()
    
    def update_particles(self):
        """Update particles"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['z'] += p['vz']
            p['life'] -= 0.01
            
            if p['life'] <= 0:
                angle = random.uniform(0, 2 * math.pi)
                elevation = random.uniform(0, math.pi)
                p['x'] = 0
                p['y'] = 0
                p['z'] = 0
                p['vx'] = math.cos(angle) * math.cos(elevation) * 0.05
                p['vy'] = math.sin(elevation) * 0.05
                p['vz'] = math.sin(angle) * math.cos(elevation) * 0.05
                p['life'] = 1.0
    
    def render_frame(self):
        """Render frame (optimized)"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -8)
        
        self.time += 0.016
        self.rotation += 0.5
        
        
        self.frame_count += 1
        if self.frame_count % 2 == 0:  
            self.rotation += 0.5
        
        glRotatef(self.rotation * 0.3, 0, 1, 0)
        glRotatef(self.rotation * 0.2, 1, 0, 0)
        
        self.update_particles()
        
        # Get color
        if self.state == "listening":
            color = [1, 0.84, 0]
        elif self.state == "processing":
            color = [1, 0.5, 0]
        elif self.state == "responding":
            color = [0, 1, 1]
        else:
            color = [0, 1, 0.8]
        
        # Draw (reduced complexity)
        self.draw_sphere_wireframe(1.5, color)
        self.draw_rings(color)
        self.draw_particles(color)
        
        pygame.display.flip()
        self.clock.tick(30) 
    
    def set_state(self, new_state):
        """Set state"""
        self.state = new_state
    
    def run(self):
        """Main loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
            
            self.render_frame()
        
        pygame.quit()

# ==================== JARVIS UI ====================
class JarvisUI:
    """Main UI"""
    def __init__(self):
        self.renderer = None
        self.start_renderer()
    
    def start_renderer(self):
        """Start renderer"""
        def run():
            try:
                self.renderer = JarvisHolographicCore(1600, 900)
                self.renderer.run()
            except Exception as e:
                print(f"Renderer error: {e}")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        time_module.sleep(1)
    
    def update_status(self, status):
        """Update status"""
        if self.renderer:
            if "listening" in status.lower():
                self.renderer.set_state("listening")
            elif "processing" in status.lower():
                self.renderer.set_state("processing")
            elif "responding" in status.lower():
                self.renderer.set_state("responding")
            else:
                self.renderer.set_state("standby")
    
    def update_text(self, text):
        pass
    
    def update_response(self, response):
        pass
    
    def add_to_history(self, command):
        pass
    
    def show(self):
        pass

def launch_advanced_gui(callbacks=None):
    ui = JarvisUI()
    if callbacks:
        ui.callbacks = callbacks
    return ui
