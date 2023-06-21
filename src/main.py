import pygame as pg
import sys
from settings import *
import math
import time as t

_ = False
map = [
[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]],
[[1],[_],[_],[_],[1],[1],[_],[_],[_],[1],[_],[_],[1]],
[[1],[_],[1],[_],[_],[1],[1],[1],[_],[1],[_],[_],[1]],
[[1],[_],[1],[_],[_],[_],[_],[_],[_],[1],[1],[_],[1]],
[[1],[_],[1],[1],[1],[1],[_],[_],[_],[_],[_],[_],[1]],
[[1],[_],[_],[_],[_],[1],[_],[1],[_],[_],[1],[_],[1]],
[[1],[1],[_],[1],[_],[1],[1],[1],[_],[_],[_],[_],[1]],
[[1],[_],[_],[1],[_],[1],[_],[_],[_],[1],[_],[1],[1]],
[[1],[_],[_],[1],[_],[1],[_],[_],[1],[1],[_],[_],[1]],
[[1],[_],[_],[1],[1],[1],[_],[_],[_],[1],[1],[_],[1]],
[[1],[_],[_],[_],[1],[_],[_],[1],[_],[1],[1],[_],[1]],
[[1],[_],[1],[1],[1],[_],[1],[1],[_],[_],[1],[_],[1]],
[[1],[_],[_],[1],[_],[_],[1],[_],[_],[_],[1],[_],[1]],
[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]],
]

class GAME_PROJET:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0,0), vsync=1)
        self.clock = pg.time.Clock()
        self.RES = self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.RAY_WIDTH_3D = self.WIDTH / NUM_RAYS

        # init stuff
        self.px, self.py = SPAWN_POINT
        self.pa = INIT_ANGLE
        self.PAN_Z_AXIS = PAN_Z_AXIS
        self.last_time = t.time()
        self.delta_time = t.time()
        self.menu_loop()

    def parse_map_and_init(self):
        self.grid_coords = []
        for row, i in enumerate(map):
            for column, j in enumerate(i):
                if j[0]:
                    self.grid_coords.append([row, column])

    def align_grid(self,x, y,flog = True):
        x -= x % 100
        y -= y % 100
        x = x/100
        y = y/100
        if flog: 
            return [x, y] not in self.grid_coords
        else:
            return x, y

    def win_condition(self):
        tu = self.align_grid(self.px, self.py, flog=False)
        if tu[0] >= 10 and tu[1] < 2:
            self.run = False

    def timer(self):
        self.elapsed_time = t.time() - self.offset
        if self.elapsed_time > TIMER:
            self.screen.fill('black')
            you_lose = self.font_b.render('GAME OVER!', True, (0xFF,0x00, 0x00))
            text_rect = you_lose.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))
            self.screen.blit(you_lose, text_rect)
            pg.display.flip()
            pg.time.delay(5000)
            self.dol()
        countdown = round(-1*(self.elapsed_time - TIMER), 2)
        text = self.font_b.render(str(countdown), True ,(0xFF, 0, 0))
        self.screen.blit(text, (self.timer_pos))

    def game_update(self):
        self.screen.fill('black')   
        self.update_player_pos()
        self.cast_rays()
    #    self.win_condition() #Part of the objective for the game, feel free to uncomment it and try it out
    #    self.timer()         
        pg.display.flip()

    def update_player_pos(self):
        dx = 0
        dy = 0
        cos_a = math.cos(self.pa)
        sin_a = math.sin(self.pa)
        self.playa_sp = PLAYER_SPEED * self.delta_time
        self.playa_rot_sp = PLAYER_ROT_SPEED * self.delta_time
        speed_cos_a = self.playa_sp * cos_a
        speed_sin_a = self.playa_sp * sin_a
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.dol()
        if keys[pg.K_w]:
            dx += speed_cos_a
            dy += speed_sin_a
        if keys[pg.K_s]:
            dx -= speed_cos_a
            dy -= speed_sin_a
        if keys[pg.K_a]:
            dx += speed_sin_a
            dy -= speed_cos_a
        if keys[pg.K_d]:
            dx -= speed_sin_a
            dy += speed_cos_a
        
        magnitude = math.sqrt(dx**2 + dy**2)

        if magnitude > self.playa_sp:
            dx = (dx / magnitude) * self.playa_sp
            dy = (dy / magnitude) * self.playa_sp

        if keys[pg.K_RIGHT]:
            self.pa += self.playa_rot_sp
            if self.pa > math.tau:
                self.pa += math.tau
        if keys[pg.K_LEFT]:
            self.pa -= self.playa_rot_sp
            if self.pa < math.tau:
                self.pa += math.tau

        if keys[pg.K_UP]:
            self.PAN_Z_AXIS += 10
            if self.PAN_Z_AXIS > 800:
                self.PAN_Z_AXIS = 800
        if keys[pg.K_DOWN]:
            self.PAN_Z_AXIS -= 10
            if self.PAN_Z_AXIS < 0:
                self.PAN_Z_AXIS = 0
        if self.align_grid((self.px + dx),self.py):
            self.px += dx 
        if self.align_grid(self.px,(self.py + dy)):
            self.py += dy
    def cast_rays(self):
        rect_x_pos = 0
        xm, ym = self.align_grid(self.px, self.py, flog=False)
        ra = self.pa - r_HALF_FOV
        for i in range(NUM_RAYS - 1):
            if ra == 0:
                ra += 0.00001
            cos_a = math.cos(ra)
            sin_a = math.sin(ra)

            #HORIZONTAL
            y_hor, dy = (ym + 1, 1) if sin_a > 0 else (ym - 1e-6, -1)
            depth_hor = (y_hor*100 - self.py) / sin_a
            x_hor = self.px + depth_hor * cos_a

            delta_depth = dy*100 / sin_a
            dx = delta_depth * cos_a
            for j in range(MAX_DEPTH):
                tile_hor = x_hor, y_hor
                if not self.align_grid(tile_hor[0], tile_hor[1]*100):
                    break
                depth_hor += delta_depth
                x_hor += dx
                y_hor += dy

            # VERTICAL
            x_vert, dx = (xm + 1, 1) if cos_a > 0 else (xm - 1e-6, -1)
            depth = (x_vert*100 - self.px) / cos_a
            y_vert = sin_a * depth + self.py
            d_depth = dx*100 / cos_a
            dy = d_depth * sin_a    
            for t in range(MAX_DEPTH):
                tile_vert = x_vert, y_vert
                if not self.align_grid(tile_vert[0]* 100, tile_vert[1]):
                    break
                x_vert += dx
                y_vert += dy 
                depth += d_depth

            if depth < depth_hor:
                fin_depth = depth
            else:
                fin_depth = depth_hor
            
            ca = self.pa - ra
            if ca < 0:
                ca += math.tau
            if ca > math.tau:
                ca -= math.tau

            line_c =(100*800)/fin_depth
            if line_c > 800:
                line_c = 800
            fin_depth = fin_depth * math.cos(ca)
            lineH=(100*800)/fin_depth 
            if (lineH > 1000):
                lineH = 1000
            light_col_val = int((line_c * 255)/800) - 50
            if light_col_val < 0:
                light_col_val = 0
            if light_col_val > 200:
                light_col_val = 200

            lineO=self.PAN_Z_AXIS-lineH/2
          #  pg.draw.rect(self.screen, 'black', (rect_x_pos, 0,RAY_WIDTH_3D, lineO), 0) # SKY
          #  pg.draw.rect(self.screen, 'black', (rect_x_pos, lineH+lineO,RAY_WIDTH_3D, HEIGHT-(lineH+lineO)), 0) # FLOOR
            pg.draw.rect(self.screen, pg.Color(light_col_val, light_col_val, light_col_val), (rect_x_pos,lineO, self.RAY_WIDTH_3D, lineH), 0) # WALL
            rect_x_pos += self.RAY_WIDTH_3D
            ra += r_DELTA_RA

    def caption(self):
        self.clock.tick(0)
        fps = self.clock.get_fps()
        pg.display.set_caption("Busters 9000    -    FPS:{:.2f}".format(fps))

    def uncap_speed_fps(self):
        current_time = t.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time

    def dol(self):
        pg.quit()
        sys.exit()

    def menu_loop(self):
        
        #GUI Start menu, feel free to uncomment and try it out
        '''
        self.font_b = pg.font.Font('assets/LEXEND-BLACK.ttf', 140)
        rectbuttons_width = self.WIDTH//4
        rectbuttons_height = self.HEIGHT//8
        padding_b_y = rectbuttons_height//6
        padding_b_x = rectbuttons_width//3
        button_x = self.WIDTH//2 - (rectbuttons_width//2)
        Text_x =self.WIDTH//4
        background_obj_unscaled = pg.image.load('assets/BG.webp')
        background_obj_scaled = pg.transform.scale(background_obj_unscaled, (self.WIDTH, self.HEIGHT))
        button_texture = pg.image.load('assets/Bt.png')
        button_texture.set_colorkey((255, 255, 255))
        button_texture_scaled = pg.transform.scale(button_texture, (rectbuttons_width, rectbuttons_height))
        text = self.font_b.render('BUSTER 9000', True, (0xAD, 0x1F, 0x9A))
        text_y = text.get_width()
        text_scaled = pg.transform.scale(text, (text_y, 300))
        text_rect = text_scaled.get_rect(center=(self.WIDTH/2, self.HEIGHT/2 - 150))
        # stupid optimisations that adds lines of codes but prevents expensive render every iteration
        b1_unscaled_b = self.font_b.render('PLAY', True, (0xFF, 0xFF, 0xFF))
        b2_unscaled_b = self.font_b.render('QUIT', True, (0xFF, 0xFF, 0xFF))
        # it is useless to use a for loop here
        b1_b = pg.transform.scale(b1_unscaled_b, (rectbuttons_width - padding_b_x, rectbuttons_height - padding_b_y))
        b2_b = pg.transform.scale(b2_unscaled_b, (rectbuttons_width - padding_b_x, rectbuttons_height - padding_b_y))
        b1_unscaled_r = self.font_b.render('PLAY', True, (0x00, 0x00, 0x00))
        b2_unscaled_r = self.font_b.render('QUIT', True, (0x00, 0x00, 0x00))
        b1_r = pg.transform.scale(b1_unscaled_r, (rectbuttons_width - padding_b_x, rectbuttons_height - padding_b_y))
        b2_r = pg.transform.scale(b2_unscaled_r, (rectbuttons_width - padding_b_x, rectbuttons_height - padding_b_y))

        selected = 0

        while True:
            self.screen.fill('black')
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                self.dol()
            if keys[pg.K_RETURN]:
                if selected == 0:
                    break
                self.dol()
            if keys[pg.K_UP]:
                selected = 0
            if keys[pg.K_DOWN]:
                selected = 1
            # textures
            self.screen.blit(background_obj_scaled, (0, 0))
            self.screen.blit(button_texture_scaled, (button_x, 500))
            self.screen.blit(button_texture_scaled, (button_x, 650))
            self.screen.blit(text_scaled, text_rect)
            if selected == 1:
                b1 = b1_b
                b2 = b2_r
            else:
                b1 = b1_r
                b2 = b2_b
            self.screen.blit(b1, (button_x + padding_b_x//2, 500 + padding_b_y//2))
            self.screen.blit(b2, (button_x + padding_b_x//2, 650 + padding_b_y//2))    
            self.caption()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.dol()
'''

        self.parse_map_and_init()
        self.run = True
        self.offset = t.time()
        self.timer_pos = (self.WIDTH - self.WIDTH//3), (self.HEIGHT - self.HEIGHT//4)
        while self.run:
            self.uncap_speed_fps()
            self.caption()
            self.game_update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.dol()
        '''
        Win screen, uncomment it along with the other peices of objective code to try it out            
        self.screen.fill('black')
        you_win = self.font_b.render('You Win!', True, (0xFF,0xFF, 0xFF))
        text_rect = you_win.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))
        self.screen.blit(you_win, text_rect)
        pg.display.flip()
        pg.time.delay(5000)
        self.menu_loop()
        '''

if __name__ == '__main__':
    game = GAME_PROJET()

