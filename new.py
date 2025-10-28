import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:/images/animated_characters/robot/robot_idle.png", .8)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.speed = 5

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "New Gamee")
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")
        self.background_color = arcade.color.AMAZON
        
        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.crystals_list = arcade.SpriteList(use_spatial_hash=True)
        self.spikes_list = arcade.SpriteList(use_spatial_hash=True)

        self.create_walls()
        self.create_spikes()
        #self.create_crystals()
    def create_walls(self):
    
        walls_position = [(SCREEN_WIDTH / 2 - 125, -30), (SCREEN_WIDTH / 2 - 250, -30), (25, -30), (SCREEN_WIDTH / 2, -30), (SCREEN_WIDTH / 2 + 125, -30), (SCREEN_WIDTH / 2 + 250, -30), (SCREEN_WIDTH - 25, -30), 
                          (SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT +30), (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT +30), (25, SCREEN_HEIGHT +30), (SCREEN_WIDTH / 2, SCREEN_HEIGHT +30), (SCREEN_WIDTH / 2 + 125, SCREEN_HEIGHT +30), (SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT +30), (SCREEN_WIDTH - 25, SCREEN_HEIGHT +30), 
                          (-30, SCREEN_HEIGHT / 2 - 125), (-30, SCREEN_HEIGHT / 2 - 250), (-30, SCREEN_HEIGHT / 2), (-30, SCREEN_HEIGHT / 2 + 125), (-30, SCREEN_HEIGHT / 2 + 250), 
                          (SCREEN_WIDTH +30, SCREEN_HEIGHT / 2 - 125), (SCREEN_WIDTH +30, SCREEN_HEIGHT / 2 - 250), (SCREEN_WIDTH +30, SCREEN_HEIGHT / 2), (SCREEN_WIDTH +30, SCREEN_HEIGHT / 2 + 125), (SCREEN_WIDTH +30, SCREEN_HEIGHT / 2 + 250),
      ]
        for x, y in walls_position:
            wall = arcade.Sprite(":resources:/images/tiles/boxCrate.png")
            wall.center_x = x
            wall.center_y = y
            self.wall_list.append(wall)
    
    def create_spikes(self):
        spikes_position = [(90, 450),
        (450, 100),
                      (200, 300),
                      (280,350),
                      (300,550),
                      (550,350),
                      (650,460),
                      (600,280),
                      (750,350),
                      (400,200),
                      (350,280)]
        for x,y in spikes_position:
            spike = arcade.Sprite(":resources:/images/tiles/spikes.png", 0.8)
            spike.center_x = x
            spike.center_y = y
            self.spikes_list.append(spike)

    #def reset(self):


    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.player_list.draw()
        self.wall_list.draw()
        self.spikes_list.draw()
    def on_update(self, delta_time):
        self.player.center_x += self.player.change_x
        self.player.center_y += self.player.change_y

        wall_hit = arcade.check_for_collision_with_list(self.player, self.wall_list)
        for wall in wall_hit:
            if self.player.change_y > 0:
                self.player.top = wall.bottom
            elif self.player.change_y < 0:
                self.player.bottom = wall.top
            if self.player.change_x > 0:
                self.player.right = wall.left
            elif self.player.change_x < 0:
                self.player.left = wall.right
        
        spikes_hit = arcade.check_for_collision_with_list(self.player, self.spikes_list)
        #for spike in spikes_hit:

    def on_key_press(self, key, modifiers):
        match key:
            case arcade.key.A:
                self.player.change_x = -self.player.speed
            case arcade.key.D:
                self.player.change_x = self.player.speed
            case arcade.key.W:
                self.player.change_y = self.player.speed
            case arcade.key.S:
                self.player.change_y = -self.player.speed
    def on_key_release(self, key, modifiers):
        match key:
            case arcade.key.A | arcade.key.D:
                self.player.change_x = 0
            case arcade.key.W | arcade.key.S:
                self.player.change_y = 0
Window = MyGame()
arcade.run()