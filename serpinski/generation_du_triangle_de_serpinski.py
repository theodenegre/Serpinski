import turtle, random as rd
from winsound import Beep

taille = 1000

# Créer une fenêtre de dessin
fenetre = turtle.Screen()

# Créer une tortue
tortue = turtle.Turtle()
tortue.pensize(2)
tortue.speed(0)
tortue.hideturtle()
turtle.tracer(True)

# Définir les positions des sommets du triangle
x_bg, y_bg = -taille / 2, -taille / 4 * 3 ** .5
x_bd, y_bd = x_bg + taille, y_bg
x_h, y_h = x_bd - taille / 2, y_bd + taille / 2 * 3 ** .5
sommets = [
    (x_bg, y_bg),
    (x_bd, y_bd),
    (x_h, y_h)
]


def positionner_tortue():
    # Positionner la tortue en bas à gauche du triangle
    tortue.penup()
    tortue.goto(x_bg, y_bg)
    tortue.pendown()


def triangle(tortue):
    # Dessiner les côtés du triangle
    tortue.goto(x_bd, y_bd)
    tortue.goto(x_h, y_h)
    tortue.goto(x_bg, y_bg)


def is_in_triangle(x, y):
    # Vérifier si le point est dans le triangle
    mg = (y_h - y_bg) / (x_h - x_bg)
    md = (y_bd - y_h) / (x_bd - x_h)
    pg = y_bg - mg * x_bg
    pd = y_h - md * x_h
    return y >= y_bg and mg * x - y + pg >= 0 and md * x - y + pd >= 0


def draw_lines():
    mg = (y_h - y_bg) / (x_h - x_bg)
    md = (y_bd - y_h) / (x_bd - x_h)
    pg = y_bg - mg * x_bg
    pd = y_h - md * x_h
    x1, x2 = 500, -500
    tortue.goto(x1, mg * x1 + pg)
    tortue.goto(x2, mg * x2 + pg)
    tortue.penup()
    tortue.goto(x1, y_bg)
    tortue.pendown()
    tortue.goto(x2, y_bg)
    tortue.penup()
    tortue.goto(x1, md * x1 + pd)
    tortue.pendown()
    tortue.goto(x2, md * x2 + pd)


def first_point_in_the_middle():
    # Choisir le premier point
    x = rd.randrange(-taille // 2, taille // 2)
    y = rd.randrange(int(-taille / 4 * 3 ** .5),
                     int(y_bd + taille / 2 * 3 ** .5))
    while not is_in_triangle(x, y):
        x = rd.randrange(-taille // 2, taille // 2)
        y = rd.randrange(int(-taille / 4 * 3 ** .5),
                         int(y_bd + taille / 2 * 3 ** .5))
    tortue.penup()
    tortue.goto(x, y)
    tortue.pendown()
    return x, y


def choose_sommet():
    # Choisir un sommet
    return rd.choice(sommets)


def next_point(x, y, sommet, color=None, draw=True):
    # Choisir le prochain point
    x1, y1 = sommet
    x = (x + x1) / 2
    y = (y + y1) / 2
    if color is None:
        color = get_colors(x, y)
    color = rgb_to_hex(color[0], color[1], color[2])
    if draw:
        tortue.penup()
        tortue.pencolor(color)
        tortue.goto(x, y)
        tortue.pendown()
        tortue.goto(x, y)
    return x, y


def get_max_distance():
    return y_h - y_bg


def get_distance_to_sides(x, y):
    # Calculer la distance entre le point et les côtés du triangle
    mg = (y_h - y_bg) / (x_h - x_bg)
    md = (y_bd - y_h) / (x_bd - x_h)
    pg = y_bg - mg * x_bg
    pd = y_h - md * x_h
    return abs(mg * x - y + pg), abs(md * x - y + pd), abs(y - y_bg)


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def get_colors(x, y):
    max_distance = get_max_distance()
    d = get_distance_to_sides(x, y)
    r = int(255/2 * d[0] / max_distance)
    g = int(255/2 * d[1] / max_distance)
    b = int(255/2 * d[2] / max_distance)
    return r, g, b


def first_point_in_random_corner():
    point = rd.choice(sommets)
    tortue.penup()
    tortue.goto(point)
    tortue.pendown()
    return point


def draw_serpinski_random_center():
    x, y = first_point_in_the_middle()
    x, y = next_point(x, y, choose_sommet(), draw=False)
    for i in range(100):
        color = get_colors(x, y)
        x, y = next_point(x, y, choose_sommet(), color, draw=False)

    i = 100
    while True:
        color = get_colors(x, y)
        if i % 100 == 0:
            print(i)
        x, y = next_point(x, y, choose_sommet(), color, draw=True)
        i += 1


def draw_serpinski_from_corner_color_delayed():
    x, y = first_point_in_random_corner()
    x, y = next_point(x, y, choose_sommet(), draw=False)
    color = get_colors(x, y)
    for i in range(100):
        x, y = next_point(x, y, choose_sommet(), color, draw=False)
        color = get_colors(x, y)

    for i in range(100, 100000):
        if i % 100 == 0:
            print(i)
        x, y = next_point(x, y, choose_sommet(), color, draw=True)
        color = get_colors(x, y)

if __name__ == '__main__':
    draw_serpinski_random_center()
    # draw_serpinski_from_corner_color_delayed()

    for beep in range(3):
        Beep(300, 300)

# Attendre que l'utilisateur ferme la fenêtre de dessin
fenetre.mainloop()

