from math import *

# print(pow(8, 2) * pi - pow(12, 2))

angle = -90
vector = (0, 5)
x = round(vector[0] * cos(angle) - vector[1] * sin(angle))
y = round(vector[0] * sin(angle) + vector[1] * cos(angle))

print(x, y)