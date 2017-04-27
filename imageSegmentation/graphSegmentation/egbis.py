from PIL import Image
import sys
import os
from random import randint

from numpy import sqrt
# sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
# from graph import build_graph, segment_graph
# from smooth_filter import gaussian_grid, filter_image
from scipy.signal import convolve2d
from numpy import *

class Node:
    def __init__(self, parent, rank=0, size=1):
        self.parent = parent
        self.rank = rank
        self.size = size

    def __repr__(self):
        return '(parent=%s, rank=%s, size=%s)' % (self.parent, self.rank, self.size)

class Forest:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.num_sets = num_nodes

    def size_of(self, i):
        return self.nodes[i].size

    def find(self, n):
        temp = n
        while temp != self.nodes[temp].parent:
            temp = self.nodes[temp].parent

        self.nodes[n].parent = temp
        return temp

    def merge(self, a, b):
        if self.nodes[a].rank > self.nodes[b].rank:
            self.nodes[b].parent = a
            self.nodes[a].size = self.nodes[a].size + self.nodes[b].size
        else:
            self.nodes[a].parent = b
            self.nodes[b].size = self.nodes[b].size + self.nodes[a].size

            if self.nodes[a].rank == self.nodes[b].rank:
                self.nodes[b].rank = self.nodes[b].rank + 1

        self.num_sets = self.num_sets - 1

    def print_nodes(self):
        for node in self.nodes:
            print (node)

def create_edge(img, width, x, y, x1, y1, diff):
    vertex_id = lambda x, y: y * width + x
    w = diff(img, x, y, x1, y1)
    return (vertex_id(x, y), vertex_id(x1, y1), w)

def build_graph(img, width, height, diff, neighborhood_8=False):
    graph = []
    for y in range(height):
        for x in range(width):
            if x > 0:
                graph.append(create_edge(img, width, x, y, x-1, y, diff))

            if y > 0:
                graph.append(create_edge(img, width, x, y, x, y-1, diff))

            if neighborhood_8:
                if x > 0 and y > 0:
                    graph.append(create_edge(img, width, x, y, x-1, y-1, diff))

                if x > 0 and y < height-1:
                    graph.append(create_edge(img, width, x, y, x-1, y+1, diff))

    return graph

def remove_small_components(forest, graph, min_size):
    for edge in graph:
        a = forest.find(edge[0])
        b = forest.find(edge[1])

        if a != b and (forest.size_of(a) < min_size or forest.size_of(b) < min_size):
            forest.merge(a, b)

    return  forest

def segment_graph(graph, num_nodes, const, min_size, threshold_func):
    weight = lambda edge: edge[2]

    forest = Forest(num_nodes)
    sorted_graph = sorted(graph, key=weight)
    threshold = [threshold_func(1, const)] * num_nodes

    for edge in sorted_graph:
        parent_a = forest.find(edge[0])
        parent_b = forest.find(edge[1])
        a_condition = weight(edge) <= threshold[parent_a]
        b_condition = weight(edge) <= threshold[parent_b]

        if parent_a != parent_b and a_condition and b_condition:
            forest.merge(parent_a, parent_b)
            a = forest.find(parent_a)
            threshold[a] = weight(edge) + threshold_func(forest.nodes[a].size, const)

    return remove_small_components(forest, sorted_graph, min_size)

def gaussian_grid(sigma, alpha=4):
    sig = max(sigma, 0.01)
    length = int(math.ceil(sig * alpha)) + 1
    m = length / 2
    n = m + 1
    x, y = mgrid[-m:n,-m:n]
    g = exp(m ** 2) * exp(-0.5 * (x**2 + y**2))
    return g / g.sum()

def filter_image(image, mask):
    layer = asarray(image).astype('float')
    layer = convolve2d(layer, mask, mode='same')
    #layer = convolve2d(layer, mask, mode='same')
    return layer


def diff_rgb(img, x1, y1, x2, y2):
    r = (img[0][x1, y1] - img[0][x2, y2]) ** 2
    g = (img[1][x1, y1] - img[1][x2, y2]) ** 2
    b = (img[2][x1, y1] - img[2][x2, y2]) ** 2
    return sqrt(r + g + b)

def diff_grey(img, x1, y1, x2, y2):
    v = (img[x1, y1] - img[x2, y2]) ** 2
    return sqrt(v)

def threshold(size, const):
    return (const / size)

def generate_image(forest, width, height):
    random_color = lambda: (int(randint(0, 255)), int(randint(0, 255)), int(randint(0, 255)))
    colors = [random_color() for i in range(width*height)]

    img = Image.new('RGB', (width, height))
    im = img.load()
    for y in range(height):
        for x in range(width):
            comp = forest.find(y * width + x)
            im[x, y] = colors[comp]

    return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)

def segmentateRun(sigma, neighbor, k, min_size, imgPath, outImagePath):
    image_file = Image.open(imgPath)
    size = image_file.size
    print ('Image info: ', image_file.format, size, image_file.mode)
    grid = gaussian_grid(sigma)

    if image_file.mode == 'RGB':
        image_file.load()
        r, g, b = image_file.split()

        r = filter_image(r, grid)
        g = filter_image(g, grid)
        b = filter_image(b, grid)

        smooth = (r, g, b)
        diff = diff_rgb
    else:
        smooth = filter_image(image_file, grid)
        diff = diff_grey

    graph = build_graph(smooth, size[1], size[0], diff, neighbor == 8)
    forest = segment_graph(graph, size[0]*size[1], k, min_size, threshold)

    image = generate_image(forest, size[1], size[0])
    image.save(outImagePath)

    print ('Number of components: %d' % forest.num_sets)

if __name__ == '__main__':
    if len(sys.argv) != 7:
        print ('Invalid number of arguments passed.')
        print ('Correct usage: python main.py sigma neighborhood K min_comp_size input_file output_file')
    else:
        neighbor = int(sys.argv[2])
        if neighbor != 4 and neighbor!= 8:
            print ('Invalid neighborhood choosed. The acceptable values are 4 or 8.')
            print ('Segmenting with 4-neighborhood...')

        image_file = Image.open(sys.argv[5])
        sigma = float(sys.argv[1])
        K = float(sys.argv[3])
        min_size = int(sys.argv[4])

        size = image_file.size
        print ('Image info: ', image_file.format, size, image_file.mode)

        grid = gaussian_grid(sigma)

        if image_file.mode == 'RGB':
            image_file.load()
            r, g, b = image_file.split()

            r = filter_image(r, grid)
            g = filter_image(g, grid)
            b = filter_image(b, grid)

            smooth = (r, g, b)
            diff = diff_rgb
        else:
            smooth = filter_image(image_file, grid)
            diff = diff_grey

        graph = build_graph(smooth, size[1], size[0], diff, neighbor == 8)
        forest = segment_graph(graph, size[0]*size[1], K, min_size, threshold)

        image = generate_image(forest, size[1], size[0])
        image.save(sys.argv[6])

        print ('Number of components: %d' % forest.num_sets)
