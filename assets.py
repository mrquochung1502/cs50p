from do_not_modify import *


class Target(pygame.sprite.Sprite):
    def __init__(self, groups, spawn_pos):
        super().__init__(groups)

        # Surf
        self.image = pygame.Surface(DIAMETER, pygame.SRCALPHA)
        pygame.draw.aacircle(self.image, TARGET_COLOR,
                             (DIAMETER[0] / 2, DIAMETER[1] / 2), DIAMETER[0] / 2 - 1)
        self.hitbox = pygame.mask.from_surface(self.image)

        # Rect
        self.rect = self.image.get_frect(center=spawn_pos)


class TextRender:
    def __init__(self, text, size: int, color):
        self.text = text
        self.font = pygame.font.Font(None, size)
        self.surf = self.font.render(str(self.text), True, color)

    def render(self, display, pos, midleft=None, bg_color=None, to_button=False):
        if midleft:
            self.rect = self.surf.get_frect(midleft=pos)
        else:
            self.rect = self.surf.get_frect(center=pos)
        if bg_color:
            pygame.draw.rect(display, bg_color, self.rect)
        display.blit(self.surf, self.rect)
        if to_button:
            if pygame.mouse.get_just_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
                return True


class ModifyNumButton:
    def __init__(self, display, default_value: int, pos):
        self.display = display
        self.pos = pos
        self.value = default_value
        self.button_image = pygame.Surface((20, 20))

    def update_num(self, value_range=None, sep=1, bi=False):
        self.increase = TextRender('>', 40, TEXT_COLOR).render(
            self.display, (self.pos[0] + 35, self.pos[1]), to_button=True)
        self.decrease = TextRender('<', 40, TEXT_COLOR).render(
            self.display, (self.pos[0] - 35, self.pos[1]), to_button=True)

        # Binary options
        if bi:
            display_text = 'On' if self.value == True else 'Off'
            TextRender(display_text, 30, TITLE_COLOR).render(self.display, self.pos)
            if self.increase or self.decrease:
                self.value = not self.value
        else:
            TextRender(self.value, 30, TITLE_COLOR).render(self.display, self.pos)
            if self.increase and self.value + sep in value_range:
                self.value += sep
            elif self.decrease and self.value - sep in value_range:
                self.value -= sep

    def return_value(self):
        return self.value
