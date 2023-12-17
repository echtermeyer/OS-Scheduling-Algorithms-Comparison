from manim import *
from jannik import ComponentTest


with tempconfig({"quality": "medium_quality"}):
    scene = ComponentTest()
    scene.render()

