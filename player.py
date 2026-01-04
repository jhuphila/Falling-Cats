import pygame
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, window_width, window_height, scale):
        super().__init__(groups)

        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale))
        )

        self.rect = self.image.get_frect(midbottom=(window_width / 2, 600))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.window_width = window_width
        self.window_height = window_height

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.rect.center += self.direction * self.speed * dt

        screen_bounds = pygame.Rect(0, 0, self.window_width, self.window_height)
        self.rect.clamp_ip(screen_bounds)