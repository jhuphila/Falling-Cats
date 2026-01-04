import pygame


class Button:
    def __init__(self, x, y, image, scale, hover_image=None, audio=None):
        width, height = image.get_width(), image.get_height()
        self.image = pygame.transform.scale(
            image,
            (int(width * scale), int(height * scale))
        )
        self.rect = self.image.get_frect()
        self.rect.center = x, y
        self.clicked = False

        self.hover_image = hover_image if hover_image else self.image
        if hover_image:
            self.hover_image = pygame.transform.scale(
                hover_image,
                (int(hover_image.get_width() * scale), int(hover_image.get_height() * scale))
            )

        self.audio = audio

    def draw(self, surface):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        mouse_just_pressed = pygame.mouse.get_just_pressed()

        if self.rect.collidepoint(mouse_pos):
            surface.blit(self.hover_image, self.rect)

            if mouse_just_pressed[0] and not self.clicked:
                self.clicked = True
                action = True
                if self.audio:
                    self.audio.play()
        else:
            surface.blit(self.image, self.rect)

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action