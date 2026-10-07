"""
GameEngine: owns the hook, the fish and the round timer, and runs one
frame's worth of game logic.

- The player casts with a key press (see main.py -> cast()).
- Fish types come from game/fish.py.
- A round lasts ROUND_SECONDS. The timer counts frames (the game runs at a
  fixed FPS), so a round is exactly ROUND_SECONDS * FPS updates. When it
  hits zero the round is over: nothing updates, no more catches are
  possible, and a fish still on the line is NOT scored (score is only
  awarded when a fish reaches the surface). restart() starts a new round.
"""

from game.hook import Hook, IDLE
from game.fish import make_fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y, FPS

ROUND_SECONDS = 30


class GameEngine:
    def __init__(self):
        self._new_round()

    def restart(self):
        """Player pressed the restart key. Only does anything once the
        round is over, so a stray key press can't wipe a round in progress."""
        if self.game_over:
            self._new_round()

    def _new_round(self):
        """Fresh hook and fish, score 0, full timer."""
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            make_fish("minnow",    x=100, y=180, direction=1),
            make_fish("barracuda", x=500, y=250, direction=-1),
            make_fish("minnow",    x=400, y=320, direction=-1),
            make_fish("barracuda", x=200, y=400, direction=1),
        ]
        self.hooked_fish = None
        self.score = 0
        self.frames_left = ROUND_SECONDS * FPS
        self.game_over = False

    @property
    def seconds_left(self):
        """Whole seconds remaining, rounded up (30 ... 1, then 0 at the end)."""
        return -(-self.frames_left // FPS)

    def cast(self):
        """Player pressed the cast key. No-op unless the hook is idle
        and the round is still running."""
        if not self.game_over:
            self.hook.start_cast()

    def update(self):
        if self.game_over:
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

        self.frames_left -= 1
        if self.frames_left <= 0:
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {self.seconds_left}", (WIDTH - 130, 10))

        if self.game_over:
            renderer.draw_overlay(surface)
            renderer.draw_banner(surface, font, "TIME'S UP!", y_offset=-30)
            renderer.draw_banner(surface, font, f"Final score: {self.score}")
            renderer.draw_banner(surface, font, "Press R to play again", y_offset=40)
        elif self.hook.state == IDLE:
            renderer.draw_text(surface, font, "Press SPACE to cast", (10, 40))
