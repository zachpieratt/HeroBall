import random
import math

def random_velocity(speed):

    angle = random.uniform(0,2*math.pi)

    return math.cos(angle)*speed, math.sin(angle)*speed