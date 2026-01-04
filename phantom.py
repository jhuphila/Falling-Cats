import pygame
from random import randint, uniform
from os.path import join


class Phantom(pygame.sprite.Sprite):
    LIFETIME_MS = 5000
    HITBOX_SCALE = 0.6
    GROUND_Y = 630

    def __init__(self, pos, scale, groups, phantom_sounds):
        super().__init__(groups)

        self.phantom_sounds = phantom_sounds
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = 300
        self.start_time = pygame.time.get_ticks()

        self.image = pygame.image.load(join("images", "phantom.png")).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale))
        )

        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_frect(center=pos)

        hitbox_width = self.rect.width * self.HITBOX_SCALE
        hitbox_height = self.rect.height * self.HITBOX_SCALE
        self.hitbox = pygame.FRect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.hitbox.center = self.rect.center

        if pygame.time.get_ticks() - self.start_time >= self.LIFETIME_MS:
            self.kill()

        if self.rect.bottom > self.GROUND_Y:
            self._play_death_sound()
            self.kill()

    def _play_death_sound(self):
        sound = pygame.mixer.Sound(self.phantom_sounds[randint(0, len(self.phantom_sounds) - 1)])
        sound.set_volume(0.5)
        sound.play()