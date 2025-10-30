import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 4
ENEMY_SPEED = 3

SPIKE_SPAWN = 2.0
ENEMY_SPAWN = 5.0
DIAMOND_SPAWN = 0.5

WALLS_POSITIONS = [
  # снизу
  (SCREEN_WIDTH / 2 - 125, 12.5),
  (SCREEN_WIDTH / 2 - 250, 12.5),
  (25, 12.5),
  (SCREEN_WIDTH / 2, 12.5),
  (SCREEN_WIDTH / 2 + 125, 12.5),
  (SCREEN_WIDTH / 2 + 250, 12.5),
  (SCREEN_WIDTH - 25, 12.5),
  # верх
  (SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT - 12.5),
  (25, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2 + 125, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT - 12.5),
  (SCREEN_WIDTH - 25, SCREEN_HEIGHT - 12.5),
  # слева
  (12.5, SCREEN_HEIGHT / 2 - 125),
  (12.5, SCREEN_HEIGHT / 2 - 250),
  (12.5, SCREEN_HEIGHT / 2),
  (12.5, SCREEN_HEIGHT / 2 + 125),
  (12.5, SCREEN_HEIGHT / 2 + 250),
  # справа
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 - 125),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 - 250),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 + 125),
  (SCREEN_WIDTH - 12.5, SCREEN_HEIGHT / 2 + 250),
]
DIAMONDS_POSITIONS = [(125, 450),
                    (450, 100),
                    (200, 300)]
DIAMONDS_POSITIONS_2 = [(300, 250),
                    (100, 500),
                    (600, 400)]
SPIKES_POSITIONS = [(200, 275), (500, 400), (200, 450)]
SPIKES_POSITIONS_2 = [(500, 150), (200, 500), (300, 450)]

class Player(arcade.Sprite):
  def __init__(self):
    super().__init__(":resources:/images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
    self.center_x = SCREEN_WIDTH / 2
    self.center_y = SCREEN_HEIGHT / 2
    self.speed = PLAYER_SPEED

  def reset(self):
    self.center_x = SCREEN_WIDTH / 2
    self.center_y = SCREEN_HEIGHT / 2

class Enemy(arcade.Sprite):
  # 1 - вправо, -1 - влево
  def __init__(self, wall_list, x, y, direction = 1):
    super().__init__(":resources:/images/alien/alienBlue_front.png", 0.5)
    self.center_x = x
    self.center_y = y
    self.speed = ENEMY_SPEED
    self.direction = direction
    self.direction *= -1
    self.default_values = {
      "direction": direction,
      "x": x,
      "y": y,
    }
  
    self.wall_list = wall_list
    
  def update(self, delta_time):
    self.center_x += self.speed * self.direction
    self.center_y -= self.speed / self.direction
    hits = arcade.check_for_collision_with_list(self, self.wall_list)
    for wall in hits:
        self.direction *= -1
        def exclude_zero(start,stop,exclude):
          while True:
            number = random.randint(start, stop)
            if number != exclude:
              return number
        self.direction = exclude_zero(-5,5,0)

  def reset(self):
    self.center_x = self.default_values["x"]
    self.center_y = self.default_values["y"]
    self.direction = self.default_values["direction"]

class MyGame(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "мини игра")
    arcade.set_background_color(arcade.color.AMAZON)

    self.player_list = arcade.SpriteList()
    self.wall_list = arcade.SpriteList()
    self.diamond_list = arcade.SpriteList()
    self.enemy_list = arcade.SpriteList()
    self.spike_list = arcade.SpriteList()
    
    self.player = Player()
    self.enemy = Enemy(self.wall_list, 300, 150)
    self.player_list.append(self.player)
    self.enemy_list.append(self.enemy)

    self.score = 0
    self.win = 0
    self.spawn_time_diamond = 0.0
    self.spawn_time_spike = 0.0
    self.spawn_time_enemy = 0.0
    self.diamonds_cnt = 3

    self.create_walls()
    self.create_diamonds()
    self.create_spikes()

  def create_walls(self):
    for x, y in WALLS_POSITIONS:
      wall = arcade.Sprite(":resources:/images/tiles/boxCrate.png")
      wall.center_x = x
      wall.center_y = y
      self.wall_list.append(wall)

  def create_diamonds(self, diamonds_positions = DIAMONDS_POSITIONS):
    for x, y in diamonds_positions:
      diamond = arcade.Sprite(":resources:images/items/gemBlue.png", 0.75)
      diamond.center_x = x
      diamond.center_y = y
      self.diamond_list.append(diamond)
  
  def create_spikes(self, spikes_positions = SPIKES_POSITIONS):
    for x, y in spikes_positions:
      spike = arcade.Sprite(":resources:images/tiles/spikes.png", 0.5)
      spike.center_x = x
      spike.center_y = y
      self.spike_list.append(spike)

  def next_level(self):
    self.reset(create_diamonds=False)


    self.enemy_list = arcade.SpriteList()
    self.enemy = Enemy(self.wall_list, 300, 400)
    self.enemy_list.append(self.enemy)

    self.spike_list = arcade.SpriteList()
    self.diamond_list = arcade.SpriteList()

    self.create_diamonds(diamonds_positions=DIAMONDS_POSITIONS_2)
    self.create_spikes(spikes_positions=SPIKES_POSITIONS_2)

  def reset(self, create_diamonds = True):
    self.score = 0
    self.player.reset()
    self.enemy.reset()

    self.diamond_list = arcade.SpriteList()
    if create_diamonds: self.create_diamonds()
    self.win = 0
  
  def spawn_one_diamond(self):
    diamond = arcade.Sprite(":resources:images/items/gemBlue.png", 0.75)
    diamond.center_x = random.randint(50, SCREEN_WIDTH - 50)
    diamond.center_y = random.randint(50, SCREEN_HEIGHT - 50)
    self.diamond_list.append(diamond)
  
  def spawn_one_spike(self):
    spike = arcade.Sprite(":resources:images/tiles/spikes.png", 0.5)
    spike.center_x = random.randint(50, SCREEN_WIDTH - 50)
    spike.center_y = random.randint(50, SCREEN_HEIGHT - 50)
    self.spike_list.append(spike)
  
  def spawn_one_enemy(self):
    enemy_x = random.randint(50, SCREEN_WIDTH - 50)
    enemy_y = random.randint(50, SCREEN_HEIGHT - 50)
    self.enemy = Enemy(self.wall_list, enemy_x, enemy_y)
    self.enemy_list.append(self.enemy)
  
  def on_draw(self):
    self.clear()
    self.player_list.draw()
    self.wall_list.draw()
    self.diamond_list.draw()
    self.enemy_list.draw()
    self.spike_list.draw()

    arcade.draw_text(
      f"Счёт: {self.score}",
      10, SCREEN_HEIGHT - 30,
      arcade.color.BLACK, 18, bold=True
    )

    if self.win == 1:
      arcade.play_sound(arcade.load_sound(":resources:/sounds/coin5.wav"))
    
    if self.win > 0:
      arcade.draw_text(
      "🎉 Все кристаллы собраны!",
      200, SCREEN_HEIGHT / 2,
      arcade.color.WHITE, 24, bold=True
    )

  def check_win(self):
    if self.score == self.diamonds_cnt:
      self.next_level()

  def on_update(self, delta_time):
    self.enemy_list.update()

    self.spawn_time_diamond += delta_time
    if self.spawn_time_diamond >= DIAMOND_SPAWN:
      self.spawn_one_diamond()
      self.spawn_time_diamond = 0.0
      self.diamonds_cnt += 1
    
    self.spawn_time_spike += delta_time
    if self.spawn_time_spike >= SPIKE_SPAWN:
      self.spawn_one_spike()
      self.spawn_time_spike = 0.0

    self.spawn_time_enemy += delta_time
    if self.spawn_time_enemy >= ENEMY_SPAWN:
      self.spawn_one_enemy()
      self.spawn_time_enemy = 0.0
    # Проверяем игрока по оси x
    self.player.center_x += self.player.change_x
    hits = arcade.check_for_collision_with_list(self.player, self.wall_list)
    for wall in hits:
      if self.player.change_x > 0:
        self.player.right = wall.left
      elif self.player.change_x < 0:
        self.player.left = wall.right

    # Проверяем игрока по оси y
    self.player.center_y += self.player.change_y
    hits = arcade.check_for_collision_with_list(self.player, self.wall_list)
    for wall in hits:
      if self.player.change_y > 0:
        self.player.top = wall.bottom
      elif self.player.change_y < 0:
        self.player.bottom = wall.top

    # Проверяем игрока на поднятие монет
    hit_diamonds = arcade.check_for_collision_with_list(self.player, self.diamond_list)
    for diamond in hit_diamonds:
      diamond.remove_from_sprite_lists()
      self.score += 1
      arcade.play_sound(arcade.load_sound(":resources:sounds/coin1.wav"))

    # Проверяем игрока на столкновение с врагом
    enemy_hits = arcade.check_for_collision_with_list(self.player, self.enemy_list)
    for _ in enemy_hits:
      self.reset()

    # Проверяем игрока на столкновение с шипами
    spike_list = arcade.check_for_collision_with_list(self.player, self.spike_list)
    for _ in spike_list:
      self.reset()

    self.check_win()

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

window = MyGame()
arcade.run()
