from math import pi, cos, sin, acos
def estimateTimeInstance(t, v, theta, g=9.8):
    # t is how many 100ms ellapsed after launch
    # v is initial speed, m/s
    t = t / 10.
    theta = theta / 180. * pi
    vx, vy = v * cos(theta), v * sin(theta)
    x = vx * t
    y = vy * t - 0.5 * g * t ** 2
    return (x, y)

def estimateProjection(x, y, mode=1):
    if mode is 1:
        v, theta = x, y
    else:
        y += 0.049
        v = (x**2+y**2)**0.5
        theta = acos(x/v)

    sequence = [(0, 0)]
    t = 1
    while True:
        x, y = estimateTimeInstance(t, v, theta)
        t += 1
        if y >= 0:
            sequence.append((x, y))
        else:
            break
    return sequence
