"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. Fish types are defined in FISH_TYPES; build fish with
make_fish() so speed, size, color and point value always stay in sync.
"""

import pygame

# Slow, big, low-value vs. fast, small, high-value. The hook sits at a
# fixed x, so a fast/small fish is harder to catch and pays more.
FISH_TYPES = {
    "minnow": {
        "speed": 2, "width": 36, "height": 18,
        "point_value": 10, "color": (80, 180, 220),   # blue
    },
    "barracuda": {
        "speed": 5, "width": 30, "height": 14,
        "point_value": 30, "color": (230, 120, 40),   # orange
    },
}


class Fish:
    def __init__(self, x, y, speed, width=36, height=18, point_value=10, color=(80, 180, 220)):
        self.x = float(x)
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )


def make_fish(type_name, x, y, direction=1):
    """Create a fish of the given type. direction: 1 = right, -1 = left."""
    t = FISH_TYPES[type_name]
    return Fish(
        x=x, y=y, speed=t["speed"] * direction,
        width=t["width"], height=t["height"],
        point_value=t["point_value"], color=t["color"],
    )
