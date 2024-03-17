from random import random

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

Builder.load_file("main.kv")


class GameBall(Widget):
    speed_ball = 3
    speed_up = 0.1
    size_ball = 30
    speed_x = 50
    speed_y = 50

    def __init__(self, **kwargs):
        super(GameBall, self).__init__(**kwargs)

        self.size = (self.size_ball, self.size_ball)

        with self.canvas.before:
            Color(1, 0, 0, 1)
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=lambda x, _: self.update_circle_pos(x),
                  size=lambda x, _: self.update_circle_size(x))

    def update_circle_pos(self, instance):
        self.circle.pos = instance.pos

    def update_circle_size(self, instance):
        self.circle.size = instance.size

    def reset(self, speed=1, speed_up=0.1, size_ball=30, speed_x=100, speed_y=100):
        self.speed_ball = speed
        self.speed_up = speed_up
        self.size_ball = size_ball
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = (self.size_ball, self.size_ball)
        self.pos = (0, 0)

    def change_color(self):
        self.canvas.before.children[0].rgba = (*(round(random(), 4) for _ in range(3)), 1)


class Settings(Popup):
    def __init__(self, ball, recall, **kwargs):
        super().__init__(**kwargs)
        self.ball = ball
        self.recall = recall

        item = self.ids
        item.size_ball_value.bind(value=lambda _, value: self.dynamic_size(value))
        item.speed_x_value.bind(value=lambda _, value: self.dynamic_speed_x(value))
        item.speed_y_value.bind(value=lambda _, value: self.dynamic_speed_y(value))
        item.buff_speed_value.bind(value=lambda _, value: self.dynamic_speed_up(value))

    def open(self):
        '''
        Label - Slider
        size_ball - size_ball_value
        speed_x - speed_x_value
        speed_y - speed_y_value
        buff_speed_ball -  buff_speed_value
        '''
        item = self.ids
        item.size_ball.text = str(self.ball.size_ball)
        item.speed_x.text = str(abs(int(self.ball.speed_x)))
        item.speed_y.text = str(abs(int(self.ball.speed_y)))
        item.buff_speed_ball.text = str(round(self.ball.speed_up, 2))

        item.size_ball_value.value = self.ball.size_ball
        item.speed_x_value.value = abs(self.ball.speed_x)
        item.speed_y_value.value = abs(self.ball.speed_y)
        item.buff_speed_value.value = self.ball.speed_up

        super().open()

    def reset(self):
        item = self.ids
        size_ball = round(item.size_ball_value.value, 2)
        speed_up = item.buff_speed_value.value
        speed_x = item.speed_x_value.value
        speed_y = item.speed_y_value.value

        item.curred_buff_speed.text = '1.0'

        self.recall(speed=1, speed_up=speed_up,
                    size_ball=size_ball, speed_x=speed_x, speed_y=speed_y)

    def update_speed_buff(self):
        self.ids.curred_buff_speed.text = f'{self.ball.speed_ball:.1f}'

    def dynamic_size(self, value):
        self.ids.size_ball.text = f'{value:.1f}'

    def dynamic_speed_x(self, value):
        self.ids.speed_x.text = f'{value:.0f}'

    def dynamic_speed_y(self, value):
        self.ids.speed_y.text = f'{value:.0f}'

    def dynamic_speed_up(self, value):
        self.ids.buff_speed_ball.text = f'{value:.1f}'


class GameApp(App):
    anim = None
    ball = None
    settings = None
    settings_menu = None
    clock = None

    def build(self):
        self.ball = GameBall(size_hint=(None, None))

        self.settings_menu = Settings(ball=self.ball, recall=self.recall)

        self.settings = Button(background_normal='white', background_color=(1, 1, 1, .05),
                               size_hint=(None, None), size=(50, 50), pos_hint={'right': 1, 'top': 1},
                               on_release=lambda _: self.settings_menu.open())

        place = FloatLayout()
        place.add_widget(self.settings)
        place.add_widget(self.ball)

        Clock.schedule_once(lambda *args: self.call_tick())
        return place

    def call_tick(self):
        time = self.tick()
        self.clock = Clock.schedule_once(lambda *args: self.call_tick(), timeout=time)

    def tick(self) -> float:
        self.settings_menu.update_speed_buff()
        self.ball.change_color()

        time = 1
        x, y = self.ball.pos

        speed_x = self.ball.speed_x * self.ball.speed_ball
        speed_y = self.ball.speed_y * self.ball.speed_ball
        wid_x, wid_y = Window.size

        # up - right
        if speed_y > 0 and speed_x > 0:
            if (wid_x - x - self.ball.size_ball) / speed_x < (wid_y - y - self.ball.size_ball) / speed_y:
                time = abs((wid_x - self.ball.size_ball - x) / speed_x)
                x = wid_x - self.ball.size_ball
                y = y + (time * speed_y)
                self.ball.speed_x *= -1
            else:
                time = abs((wid_y - self.ball.size_ball - y) / speed_y)
                y = wid_y - self.ball.size_ball
                x = x + (time * speed_x)
                self.ball.speed_y *= -1

        # down - right
        elif speed_y < 0 and speed_x > 0:
            if abs((wid_x - x - self.ball.size_ball) / speed_x) < abs(y / speed_y):
                time = abs((wid_x - self.ball.size_ball - x) / speed_x)
                x = wid_x - self.ball.size_ball
                y = y + (time * speed_y)
                self.ball.speed_x *= -1
            else:
                time = abs(y / speed_y)
                y = 0
                x = x + (time * speed_x)
                self.ball.speed_y *= -1

        # up - left
        elif speed_y > 0 and speed_x < 0:
            if abs((wid_y - y - self.ball.size_ball) / speed_y) < abs((x) / speed_x):
                time = abs((wid_y - self.ball.size_ball - y) / speed_y)
                y = wid_y - self.ball.size_ball
                x = x + (time * speed_x)
                self.ball.speed_y *= -1
            else:
                time = abs(x / speed_x)
                x = 0
                y = y + (time * speed_y)
                self.ball.speed_x *= -1

        # down - left
        elif speed_y < 0 and speed_x < 0:
            if x / speed_x > y / speed_y:
                time = abs(x / speed_x)
                x = 0
                y = y + (time * speed_y)
                self.ball.speed_x *= -1
            else:
                time = abs(y / speed_y)
                y = 0
                x = x + (time * speed_x)
                self.ball.speed_y *= -1

        self.anim = Animation(x=x, y=y, duration=time)
        self.anim.start(self.ball)
        print(f"time move: {float(time):.3}, move to: ({x}, {y})")
        if x < 0 or y < 0:
            raise Exception('fatal')

        self.ball.speed_ball += self.ball.speed_up
        return time

    def stop_anim(self):
        self.anim.stop(self.ball)

    def recall(self, speed=1, speed_up=0.1, size_ball=30, speed_x=100, speed_y=100):
        self.clock.cancel()
        self.anim.stop(self.ball)
        self.ball.reset(speed=speed, speed_up=speed_up,
                        size_ball=size_ball, speed_x=speed_x, speed_y=speed_y)
        self.call_tick()


if __name__ == '__main__':
    GameApp().run()
