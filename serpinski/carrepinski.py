import matplotlib.pyplot as plt
import random as rd
from math import cos, sin, pi
from time import time_ns
import os
import random
from numpy import linspace
from winsound import Beep



def draw_polygon(ax, sommets):
    polygon = plt.Polygon(sommets, closed=True, fill=None, edgecolor='black')
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


def dessiner_arbre(x, y, angle, longueur, profondeur, ax, n=5):
    """
    Dessine un arbre de n branches et de profondeur iter (niveau de récursion)
    avec matplotlib
    """
    if profondeur > 0:
        x2 = x + longueur * cos(angle)
        y2 = y + longueur * sin(angle)

        # Dessine la branche
        ax.plot([x, x2], [y, y2], color='black', lw=0.1)

        for branch in range(n):
            angle2 = angle + (branch - n // 2) * 2 * pi / n
            dessiner_arbre(x2, y2, angle2, longueur / 2, profondeur - 1, ax, n)


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
    mult = 7
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
    generate(1, 25_000_000, 6, 2, 1e-3)
    done()
