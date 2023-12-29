from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color


from random import random


class GameBall(Widget):
    def __init__(self, **kwargs):
        super(GameBall, self).__init__(**kwargs)

        # Add graphical instructions to draw a circular shape
        with self.canvas.before:
            Color(1, 0, 0, 1)  # RGBA values (1, 0, 0, 1) represent red color
            self.circle = Ellipse(pos=self.pos, size=self.size)

        # Bind the update_circle_pos method to be called when the ball's position changes
        self.bind(pos=self.update_circle_pos)

    def update_circle_pos(self, instance, value):
        self.circle.pos = instance.pos


class GameApp(App):
    speed_ball = 1
    size_ball = 30
    run_x = 100
    run_y = 100

    ball = None

    def build(self):
        self.ball = GameBall(size_hint=(None, None), size=(self.size_ball, self.size_ball))

        box = FloatLayout()
        box.add_widget(self.ball)
        Clock.schedule_once(lambda *args: self.call_tick())
        return box

    def call_tick(self):
        time = self.tick()
        Clock.schedule_once(lambda *args: self.call_tick(), timeout=time)

    def tick(self) -> float:
        time = 1
        x, y = self.ball.pos

        speed_x = self.run_x * self.speed_ball
        speed_y = self.run_y * self.speed_ball
        wid_x, wid_y = Window.size

        self.ball.canvas.before.children[0].rgba = (*(round(random(), 4) for _ in range(3)), 1)

        # up - right
        if speed_y > 0 and speed_x > 0:
            if (wid_x - x - self.size_ball)/speed_x < (wid_y - y - self.size_ball)/speed_y:
                time = abs((wid_x - self.size_ball - x)/speed_x)
                x = wid_x - self.size_ball
                y = y + (time*speed_y)
                self.run_x *= -1
            else:
                time = abs((wid_y - self.size_ball - y) / speed_y)
                y = wid_y - self.size_ball
                x = x + (time * speed_x)
                self.run_y *= -1

        # down - right
        elif speed_y < 0 and speed_x > 0:
            if abs((wid_x - x - self.size_ball)/speed_x) < abs(y/speed_y):
                time = abs((wid_x - self.size_ball - x) / speed_x)
                x = wid_x - self.size_ball
                y = y + (time * speed_y)
                self.run_x *= -1
            else:
                time = abs(y / speed_y)
                y = 0
                x = x + (time * speed_x)
                self.run_y *= -1

        # up - left
        elif speed_y > 0 and speed_x < 0:
            if abs((wid_y - y)/speed_y) < abs((x + self.size_ball)/speed_x):
                time = abs((wid_y - self.size_ball - y) / speed_y)
                y = wid_y - self.size_ball
                x = x + (time * speed_x)
                self.run_y *= -1
            else:
                time = abs(x / speed_x)
                x = 0
                y = y + (time * speed_y)
                self.run_x *= -1

        # down - left
        elif speed_y < 0 and speed_x < 0:
            if x/speed_x > y/speed_y:
                time = abs(x / speed_x)
                x = 0
                y = y + (time * speed_y)
                self.run_x *= -1
            else:
                time = abs(y / speed_y)
                y = 0
                x = x + (time * speed_x)
                self.run_y *= -1

        anim = Animation(x=x, y=y, duration=time)
        anim.start(self.ball)
        print(f"time move: {time:.3}, move to: ({x}, {y})")

        self.speed_ball += 0.1
        return time


if __name__ == '__main__':
    GameApp().run()
