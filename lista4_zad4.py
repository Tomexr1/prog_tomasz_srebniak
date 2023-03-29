import networkx as nx
from PIL import Image
import matplotlib.pyplot as plt


G = nx.complete_graph(20)
nx.draw(G)
