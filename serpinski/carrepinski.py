import matplotlib.pyplot as plt
import random as rd
from math import cos, sin, pi
from time import *
import os
import random
from numpy import linspace
from winsound import Beep
import turtle



def draw_polygon(ax, sommets):  # TODO repare this
    polygon = plt.Polygon(sommets, fill=None, edgecolor='black')
    ax.add_patch(polygon)


def choose_sommet(sommets):
    return rd.choice(sommets)


def next_point(x, y, sommet, d):
    x = (x + sommet[0]) / d
    y = (y + sommet[1]) / d
    return x, y


def simulate_points(n, sommets, d):
    x, y = 0, 0
    points = []
    for _ in range(n):
        sommet = choose_sommet(sommets)
        x, y = next_point(x, y, sommet, d)
        points.append((x, y))
    return points


def create_sommets(n, size):
    sommets = []
    for i in range(n):
        angle = 2 * i * pi / n + (5 * pi / 2)
        sommet = (size * cos(angle), size * sin(angle))
        sommets.append(sommet)
    return sommets


def precompute_points(n_iteration, n_start, n_end, step=2, size=1):
    points_list = []
    if n_start < n_end:
        n_start, n_end = n_end, n_start
    for n_sides in range(n_start, n_end - 1, -step):
        sommets = create_sommets(n_sides, size)
        points = simulate_points(n_iteration, sommets)
        points_list.append((points, n_sides))
    return points_list


def from_big_to_small(ax, points_list, n_iteration):
    for points, n_sides in points_list:
        ax.clear()
        ax.set_aspect('equal')
        ax.axis('off')
        points_x, points_y = zip(*points)
        ax.scatter(points_x, points_y, s=1e-5, color='black')
        ax.set_title(f'Polygon with {n_sides} sides and {n_iteration} points')
        plt.pause(0.5)


def update_plot(i, points_list, ax):
    points, n_sides = points_list[i]
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')
    points_x, points_y = zip(*points)
    ax.scatter(points_x, points_y, s=1e-5, color='black')
    ax.set_title(f'Polygon with {n_sides} sides and {len(points)} points')


def dessiner_arbre(x, y, angle, longueur, profondeur, ax, n=5, deno=2):
    """
    Dessine un arbre de n branches et de profondeur iter (niveau de récursion)
    avec matplotlib
    """
    if profondeur > 0:
        x2 = x + longueur * cos(angle)
        y2 = y + longueur * sin(angle)

        # Dessine la branche
        ax.plot([x, x2], [y, y2], color='black', lw=0.3)

        for branch in range(n):
            angle2 = angle + (branch - n // 2) * 2 * pi / n
            dessiner_arbre(x2, y2, angle2, longueur / deno, profondeur - 1, ax, n, deno)
    ax.set_aspect('equal')
    ax.axis('off')



def dessiner_arbre_clean(x, y, angle, longueur, profondeur, ax, n=5, deno=2):
    """
    Dessine un arbre de n branches et de profondeur iter (niveau de récursion)
    avec matplotlib
    """
    if profondeur > 0:
        # Dessine la branche, mais ignore le premier quart et le dernier quart
        x2 = x + longueur * cos(angle)
        y2 = y + longueur * sin(angle)
        # quart point
        x3 = x + longueur * cos(angle) / 4
        y3 = y + longueur * sin(angle) / 4
        # trois quart point
        x4 = x + longueur * cos(angle) * 3 / 4
        y4 = y + longueur * sin(angle) * 3 / 4

        ax.plot([x3, x4], [y3, y4], color='black', lw=0.3)


        for branch in range(n):
            angle2 = angle + (branch - n // 2) * 2 * pi / n
            dessiner_arbre_clean(x2, y2, angle2, longueur / deno, profondeur - 1, ax, n, deno)
    ax.set_aspect('equal')
    ax.axis('off')

def dessiner_arbre_variante(x, y, angle, longueur, profondeur, ax, n=5, deno=2):
    """
    Dessine un arbre de n branches et de profondeur iter (niveau de récursion)
    avec matplotlib
    """
    if profondeur > 0:
        x2 = x + longueur * cos(angle)
        y2 = y + longueur * sin(angle)

        # Dessine la branche
        ax.plot([x, x2], [y, y2], color='black', lw=0.3)

        for branch in range(n):
            angle2 = angle + (branch - n / 2) * 2 * pi / n
            dessiner_arbre(x2, y2, angle2, longueur / deno, profondeur - 1,
                           ax, n, deno)
    ax.set_aspect('equal')
    ax.axis('off')


def turtle_dessiner_arbre(x, y, angle, longueur, profondeur, tortue, n=5, deno=2):
    """
    Dessine un arbre de n branches et de profondeur iter (niveau de récursion)
    avec turtle
    """
    if profondeur > 0:
        x2 = x + longueur * cos(angle)
        y2 = y + longueur * sin(angle)

        # Dessine la branche
        tortue.goto(x2, y2)

        for branch in range(n):
            angle2 = angle + (branch - n // 2) * 2 * pi / n
            turtle_dessiner_arbre(x2, y2, angle2, longueur / deno, profondeur - 1, tortue, n, deno)


def turtle_dessiner_arbre_demi_tour(x, y, angle, longueur, profondeur, tortue, n=5, deno=2):
    """
    Dessine un arbre de n branches et de profondeur iter (niveau de récursion)
    avec turtle mais retourne sur ses pas à chaque étape
    """
    if profondeur > 0:
        x2 = x + longueur * cos(angle)
        y2 = y + longueur * sin(angle)

        # Dessine la branche
        tortue.goto(x2, y2)

        for branch in range(n):
            angle2 = angle + (branch - n // 2) * 2 * pi / n
            turtle_dessiner_arbre_demi_tour(x2, y2, angle2, longueur / deno, profondeur - 1, tortue, n, deno)
        tortue.goto(x, y)


def serpinski_pentagone(x, y, size, iter, ax):  # TODO généraliser pour les polygones
    if iter == 0:
        # fait un pentagone remplis
        for i in range(5): # TODO opti avec un seul fill
            x1 = x + size * cos(2 * pi * i / 5)
            y1 = y + size * sin(2 * pi * i / 5)
            x2 = x + size * cos(2 * pi * (i + 1) / 5)
            y2 = y + size * sin(2 * pi * (i + 1) / 5)
            x3 = x + size * cos(2 * pi * (i + 2) / 5)
            y3 = y + size * sin(2 * pi * (i + 2) / 5)
            ax.fill([x, x1, x2, x3], [y, y1, y2, y3], color='black', alpha=0.05)
    else:
        # a mi-distance entre le point actuel et chacun des sommets
        # dessiser un serpinski_pentagone pour chaque sommet
        for i in range(5):
            x1 = x + size * cos(2 * pi * i / 5 + pi/2)
            y1 = y + size * sin(2 * pi * i / 5 + pi/2)
            serpinski_pentagone(x1, y1, size / 2, iter - 1, ax)


def generate(size, n_iter: int, nbr_sides, deno, point_size):
    start = time_ns()
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')
    plt.get_current_fig_manager().resize(950, 950)

    points = simulate_points(n_iter, create_sommets(nbr_sides, size), deno)
    points_x, points_y = zip(*points)
    ax.scatter(points_x, points_y, s=point_size, color='black', linewidth=0)
    ax.set_xlim(min(points_x), max(points_x))
    ax.set_ylim(min(points_y), max(points_y))
    ax.set_title(
            f'{nbr_sides} sides {n_iter:.0e} points {deno = } {point_size = } ratio: {n_iter / point_size:.0e} {(time_ns() - start) / 1e9:.2f} seconds')

    file_name = ax.get_title().replace(' ', '_').replace(':', '') + '.png'
    file_name = "images" + os.sep + file_name
    plt.savefig(file_name, dpi=500)
    plt.close(fig)


def brute_force():
    sides_list = [3, 4, 5, 6, 7, 8, 9, 11, 21]
    deno_list = [2, 3, 4, 5, 1.9, 2.1, 2.5, 3.5, 1.5, 1.1]
    point_size_list = [1e-5, 1e-4, 1e-3, 1e-2]
    n_iter_list = [10 ** i for i in range(6, 8)]
    size_list = [10 ** i for i in range(-1, 2)]

    while True:
        size = random.choice(size_list)
        point_size = random.choice(point_size_list)
        n_iter = random.choice(n_iter_list)
        deno = random.choice(deno_list)
        nbr_sides = random.choice(sides_list)
        file_name = f'{nbr_sides} sides {n_iter:.0e} points {deno = } {point_size = }'.replace(
                ' ', '_').replace(':', '')

        # Vérifier si un fichier existant commence par file_name
        file_exists = any(
                file.startswith(file_name) for file in
                os.listdir(os.path.join("images" + os.sep + file_name)))

        if file_exists:
            print(f"File starting with {file_name} already exists.")
        else:
            local_start = time_ns()
            print(
                    f'{nbr_sides} sides {deno = } {n_iter:.0e} points {point_size = } ratio: {n_iter / point_size:.0e}',
                    end=' ')
            generate(size, n_iter, nbr_sides, deno, point_size)
            elapsed_time = (time_ns() - local_start) / 1e9
            print(f'{elapsed_time:.2f} seconds')


def done():
    """Thanks copilot"""
    mult = 3
    Beep(440, int(mult * 50))
    Beep(440, int(mult * 50))
    Beep(440, int(mult * 50))
    Beep(349, int(mult * 35))
    Beep(523, int(mult * 15))
    Beep(440, int(mult * 50))
    Beep(349, int(mult * 35))
    Beep(523, int(mult * 15))
    Beep(440, int(mult * 100))


if __name__ == '__main__':
    ax, fig = plt.subplots()

    # generate(1, 25_000_000, 6, 2, 1e-3)
    start = time_ns()
    # affiche, l'heure de début
    print(f"started at : {ctime()}")
    # dessiner_arbre(0, 0, pi / 2, 100, 7, plt.gca(), 5, (1+5**0.5)/2)
    # dessiner_arbre(0, 0, pi / 2, 100, 6, plt.gca(), 5, 2)
    # dessiner_arbre_clean(0, 0, pi / 2, 100, 8, plt.gca(), 5, 2) # 341 seconds for 7 iterations (au moins 2h pour 8)
    # dessiner_arbre_variante(0, 0, pi / 2, 100, 6, plt.gca(), 5, 2)
    serpinski_pentagone(0, 0, 100, 7, plt.gca())
    # t = turtle.Turtle()
    # t.speed(0)
    # t.hideturtle()
    # turtle_dessiner_arbre(0, -300, pi / 2, 300, 6, t, 5, 2) # 1593 seconds for 8 iterations
    # turtle_dessiner_arbre_demi_tour(0, -300, pi / 2, 300, 7, t, 5,  2)  # 3246 seconds for 8 iterations
    print((time_ns() - start) / 1e9)
    # turtle.done()
    # rends les axes egaux, ...
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.show()
    # done()
