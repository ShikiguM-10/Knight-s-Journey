import pygame
from support import import_csv_layout, import_graphics
from settings import tile_size, screen_height, screen_width
from tile import Tile, StaticTile, Crate, Coin, Tree
from enemy import Enemy
from game_data import levels
from decoration import Background
from player import Player
from particles import Particle


class Level:
    def __init__(self, current_level, surface, create_overworld, change_scores,
                 change_health, current_health, check_endgame, game_object):

        # Настройка экрана и скорость прокрутки уровня
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # Настройка текущего уровня
        self.current_level = current_level
        level_data = levels[current_level]

        # Уровень для разблокировки
        self.new_max_level = level_data['unlock']

        # Настройка создания внешнего мира навигации
        self.create_overworld = create_overworld
        level_data = levels[self.current_level]

        # Настройка ландшафта
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_group_tile(terrain_layout, 'terrain')

        # Настройка травы
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_group_tile(grass_layout, 'grass')

        # Настройка ящиков
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_group_tile(crate_layout, 'crates')

        # Настройка монет
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_group_tile(coin_layout, 'coins')
        self.temp_scores = 0

        # Настройка деревьев на переднем плане
        fg_trees_layout = import_csv_layout(level_data['fg trees'])
        self.fg_trees_sprites = self.create_group_tile(fg_trees_layout, 'fg trees')

        # Настройка деревьев на заднем плане
        bg_trees_layout = import_csv_layout(level_data['bg trees'])
        self.bg_trees_sprites = self.create_group_tile(bg_trees_layout, 'bg trees')

        # Настройка врагов
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprite = self.create_group_tile(enemy_layout, 'enemies')

        # Настройка ограничений для врагов
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_group_tile(constraint_layout, 'constraints')

        # Настройка игрока
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.purpose = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        self.player_on_ground = False
        self.current_health = current_health
        self.check_endgame = check_endgame

        # Настройка пользовательнского интерфейса
        self.change_scores = change_scores

        # Настройка декораций
        self.background = Background()
        level_width = len(terrain_layout[0]) * tile_size

        # Настройка частиц игрока
        self.dust_sprite = pygame.sprite.GroupSingle()

        # Настройка эффекта гибели врага
        self.death_sprites = pygame.sprite.Group()

        # Настройка привязки уровня к объекту игры
        self.game_object = game_object

        # Статус проверки прохождения финального уровня
        self.passed = False

    # Создание группы тайлов уровня
    def create_group_tile(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # Устанавливаем спрайты на блоки ландшафта
                    if type == 'terrain':
                        terrain_tile_list = import_graphics('../graphics/terrain/tileset.jpg')
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    # Устанавливаем спрайты на блоки травы
                    if type == 'grass':
                        grass_tile_list = import_graphics('../graphics/terrain/grass_tiles.png')
                        tile_surface = grass_tile_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    # Устанавливаем спрайты на блоки ящиков
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    # Ставим спрайты врагов
                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    # Ставим спрайты ограничений для врагов
                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    # Накладываем спрайты на монетки
                    if type == 'coins':
                        if col == '0':
                            sprite = Coin(tile_size, x, y,
                                          '../graphics/coin/standart', 1)
                        if col == '1':
                            sprite = Coin(tile_size, x, y,
                                          '../graphics/coin/silver', 2)

                    # Накладываем спрайты на деревья на переднем плане
                    if type == 'fg trees':
                        if col == '1':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/onetree', 85)
                        if col == '2':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/twotree', 118)
                        if col == '3':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/threetree', 133)
                        if col == '4':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/fourtree', 55)
                        if col == '5':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/siztree', 100)
                        if col == '6':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/fivetree', 82)

                    # Накладываем спрайты на деревья на заднем плане
                    if type == 'bg trees':
                        if col == '0':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/seventree', 45)
                        if col == '1':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/onetree', 85)
                        if col == '3':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/threetree', 125)
                        if col == '5':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/siztree', 150)
                        if col == '6':
                            sprite = Tree(tile_size, x, y,
                                          '../graphics/terrain/trees/fivetree', 82)

                    sprite_group.add(sprite)

        return sprite_group

    # Проверка на столкновение с монетами
    def check_coin_collision(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,
                                                     self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.temp_scores += coin.value
                self.change_scores(coin.value)

    # Проверка на столкновение с врагом
    def check_enemy_collision(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,
                                                       self.enemies_sprite, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    exploision_sprite = Particle(enemy.rect.center, 'exploision')
                    self.death_sprites.add(exploision_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def input(self):
        keys = pygame.key.get_pressed()

        # секретная конпка для быстрого прохождения уровня
        if keys[pygame.K_p]:
            self.create_overworld(self.current_level, self.new_max_level)

        # конпка выхода с уровня
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)

    def isdeath(self):
        if self.player.sprite.rect.top > screen_height:
            self.player.sprite.get_damage(-100)
            self.change_scores(-self.temp_scores)

    def iswin(self, game_object):
        if self.current_level == self.new_max_level and self.passed:
            game_object.status = "end"

        if pygame.sprite.spritecollide(self.player.sprite, self.purpose, False):
            if self.current_level == self.new_max_level:
                self.passed = True
            else:
                self.create_overworld(self.current_level, self.new_max_level)

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == '0':
                    sprite = Player((x, y), self.display_surface, self.jump_particles,
                                    change_health)
                    self.player.add(sprite)
                if col == '1':
                    hat_surface = pygame.image.load('../graphics/character/end.jpg').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.purpose.add(sprite)

    # Проверка, находился ли персонаж на земле
    def get_player_onground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # Анимация чатсиц приземления
    def create_land_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(1, 17)
            else:
                offset = pygame.math.Vector2(-1, 17)
            land_particles = Particle(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(land_particles)

    # Анимация частиц прыжка
    def jump_particles(self, position):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(10, 5)
        else:
            position += pygame.math.Vector2(10, -5)
        jump_part_sprite = Particle(position, 'jump')
        self.dust_sprite.add(jump_part_sprite)

    # Вертикальная коллизия игрока
    def vertical_move(self):
        player = self.player.sprite
        player.apply_gravity()
        collide_sprites_groups = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        for sprite in collide_sprites_groups:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_celling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    # Горизонтальная коллизия игрока
    def horizontal_move(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collide_sprites_groups = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        for sprite in collide_sprites_groups:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    # Перемещение камеры при приближении игрока к концу экрана
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 4

    # Проверка столкновений врагов с их ограничителями
    def enemy_move_reverse(self):
        for enemy in self.enemies_sprite.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        self.input()

        # Отображение заднего фона
        self.background.draw(self.display_surface)

        # Отображение деревьев на заднем плане
        self.bg_trees_sprites.update(self.world_shift)
        self.bg_trees_sprites.draw(self.display_surface)

        # Отображение частиц приземления и прыжка
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Отображаем ландшафт
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # Отображение врагов, ограничений для них и частиц для смерти
        self.enemies_sprite.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_move_reverse()
        self.enemies_sprite.draw(self.display_surface)
        self.death_sprites.update(self.world_shift)
        self.death_sprites.draw(self.display_surface)

        # Отображение ящиков
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # Отображение деревьев на переднем плане
        self.fg_trees_sprites.update(self.world_shift)
        self.fg_trees_sprites.draw(self.display_surface)

        # Отображение травы
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # Отображение монеток
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Отображение игрока и включение его перемещения
        self.player.update()
        self.horizontal_move()
        self.get_player_onground()
        self.vertical_move()
        self.create_land_particles()
        self.scroll_x()
        self.player.draw(self.display_surface)

        # Отображение конца уровня
        self.purpose.update(self.world_shift)
        self.purpose.draw(self.display_surface)

        # Проверка на проигрыш или выйгрыш
        self.isdeath()
        self.iswin(self.game_object)

        # Проверка на столкновение с врагом
        self.check_enemy_collision()

        # Проверка на стоклновение со спрайтом монетки
        self.check_coin_collision()
