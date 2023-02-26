def bgrtolab(color):
    color[0] = color[0] * 100 / 255
    color[1] = color[1] - 128
    color[2] = color[2] - 128
    pass


def labtobgr(color):
    color[0] = color[0] * 100 / 255
    color[1] = color[1] + 128
    color[2] = color[2] + 128
    pass
