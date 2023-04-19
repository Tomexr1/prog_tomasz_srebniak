"""
    Program tworzący animację losowego błądzenia agenta po grafie.
"""

import networkx as nx
import matplotlib.pyplot as plt
from random import choice, random
import os
import imageio


frames = []

# losowanie grafu
G = nx.fast_gnp_random_graph(20, 0.5)
node_position = {}
for node in G.nodes:  # ustalanie stałej pozycji wierzchołków dla gragu G
    node_position[node] = (random(), random())

# losowanie wierzchołka startowego
current_node = choice(list(G.nodes))
color_map = ['red' if node == current_node else 'blue' for node in G.nodes]

# zapisywanie 1 grafu
frames.append('frame0.png')
nx.draw(G, pos=node_position, node_color=color_map, with_labels=True)
plt.savefig('frame0.png')
plt.clf()

for i in range(50):
    # losowanie sąsiada
    neighbour = choice(list(G.neighbors(current_node)))
    # przejście do sąsiada
    color_map[current_node], color_map[neighbour] = 'blue', 'red'
    # zapisywanie kolejnych grafów
    filename = f'frame{i+1}.png'
    frames.append(filename)
    # update graph with new colormap
    nx.draw(G, pos=node_position, node_color=color_map, with_labels=True)
    plt.savefig(filename)
    plt.clf()
    # aktualizacja aktualnego wierzchołka
    current_node = neighbour

# create gif with with 2 frame per second speed

with imageio.get_writer('RandomWalk.gif', mode='I', duration=1) as writer:  # duration=1 - zmienai klatkę co sekundę
    for filename in frames:
        image = imageio.v2.imread(filename)
        writer.append_data(image)

for filename in list(frames):
    os.remove(filename)
