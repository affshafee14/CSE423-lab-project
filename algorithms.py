# Midpoint Line Drawing Algorithm (Zone 0)
def midpoint_line(x0, y0, x1, y1):
    points = []
    dx = x1 - x0
    dy = y1 - y0

    p = 2 * dy - dx
    x, y = x0, y0

    while x <= x1:
        points.append((x, y))
        x += 1
        if p < 0:
            p += 2 * dy
        else:
            y += 1
            p += 2 * dy - 2 * dx

    return points

# Zone Conversion
def zone_conversion(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0

    if abs(dx) >= abs(dy):  # dx dominates
        if dx > 0 and dy >= 0: return (x0, y0, x1, y1, 0)
        if dx < 0 <= dy: return (-x0, y0, -x1, y1, 3)
        if dx < 0 and dy < 0: return (-x0, -y0, -x1, -y1, 4)
        if dx > 0 > dy: return (x0, -y0, x1, -y1, 7)
    else:  # dy dominates
        if dy > 0 and dx >= 0: return (y0, x0, y1, x1, 1)
        if dy > 0 > dx: return (y0, -x0, y1, -x1, 2)
        if dy < 0 and dx < 0: return (-y0, -x0, -y1, -x1, 5)
        if dy < 0 <= dx: return (-y0, x0, -y1, x1, 6)

# Reverse Zone Conversion
def reverse_zone_conversion(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

# Draw a Line
def draw_line(x0, y0, x1, y1):
    converted = zone_conversion(x0, y0, x1, y1)
    x0, y0, x1, y1, zone = converted
    points = midpoint_line(x0, y0, x1, y1)
    final_points = [reverse_zone_conversion(x, y, zone) for x, y in points]

    glBegin(GL_POINTS)
    for x, y in final_points:
        glVertex2f(x, y)
    glEnd()


# Midpoint Circle Drawing Algorithm
def plot_symmetric_points(xc, yc, x, y):
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)

def midpoint_circle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    glBegin(GL_POINTS)
    plot_symmetric_points(xc, yc, x, y)

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x - 2 * y + 1

        plot_symmetric_points(xc, yc, x, y)
    glEnd()

draw_circle = lambda x, y, r: midpoint_circle(x, y, r)
