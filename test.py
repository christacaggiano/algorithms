
from pyxdameraulevenshtein import damerau_levenshtein_distance as distance
import random
import numpy as np
import itertools
import math





def avg(l):
    return sum(l)/len(l)


def avg_string(strings):
    """
    Returns the "average" string in the list
    AKA the string with the least average distance to all the other strings in the list
    :param strings: List of strings
    :return: The average string as defined above
    """
    answer = min([(y, avg([distance(y, x) for x in strings])) for y in strings], key=lambda x: x[1])[0]
    return answer


def calc_distance(a, b):
    return distance(a, b)


def kmeans(protein_strings, k):
    cents = random.sample(protein_strings, k)

    clusters = [[] for i in range(k)]
    change = True
    i = 0
    while change:
        change = False
        for s in protein_strings:

            distances = [(idx, distance(s, cent)) for idx, cent in enumerate(cents)]
            min_idx, _ = min(distances, key=lambda t: t[1])
            cluster = clusters[min_idx]
            if s not in cluster:
                cluster.append(s)
                change = True
                for idx, other_cluster in enumerate(clusters):
                    if idx != min_idx and s in other_cluster:
                        other_cluster.remove(s)
        i += 1
        cents = [avg_string(cluster) for cluster in clusters]
    return clusters


def cluster(clusters):

    size = len(clusters)
    sim_matrix = np.empty((size, size))

    for i in range(size):
        for j in range(size):
            sim_matrix[i][j] = single_linkage(clusters[i], clusters[j])

    # print(sim_matrix)
    i, j, distance = minimum_position(sim_matrix)
    return merge_clusters(i, j, clusters, size), distance


def single_linkage(cluster1, cluster2):

    tuples = list(itertools.product(cluster1, cluster2))
    distances = [distance(t[0], t[1]) for t in tuples]

    return min(distances)


def minimum_position(matrix):

    np.fill_diagonal(matrix, np.inf)
    min_loc = np.where(matrix == np.min(matrix))

    min_i = (min_loc[0])[0]
    min_j = (min_loc[1])[0]

    # print(matrix)
    # print(min_loc)
    # print(min_i)
    # print(min_j)

    return min_i, min_j, matrix.min()

def merge_clusters(i, j, clusters, size):

    merged_cluster = []
    old_clusters = []
    new_clusters_all = []

    for cluster_count in range(size):
        if cluster_count == i or cluster_count == j:
            merged_cluster += clusters[cluster_count]
        else:
            old_clusters.append(clusters[cluster_count])
    return([merged_cluster] + old_clusters)
    # print(new_clusters_all.append(old_clusters))
    # print(new_cluster_set.append(merged_cluster))



def agglomerative(strings):

    clusters = [[strings[i]] for i in range(len(strings))]
    distances = []

    max_d = 0
    max_d_loc = 0

    while len(clusters) > 1:
        clusters, distance = cluster(clusters)
        # print(len(clusters))
        distances.append(distance)
        print(clusters, distances)

        if len(distances) > 1:
            if (distances[-1] - distances[-2]) > max_d:
                max_d = (distances[-1] - distances[-2])
                max_d_loc = clusters

    print('final cluster')
    print(max_d_loc)




# strings = ["AAAA", "AGATC", "ATTTC", "GGGAAAA", "AATAA", "AAAAAAAAGGGGAAA", "GGGCQL"]
strings = ["".join([random.choice("GALMFWKQESPVICYHRNDT") for j in range(random.randint(10,20))]) for i in range(5)]
#strings = ["ABC", "AQC", "DDDD"]
# print(kmeans(strings, 20))

agglomerative(strings)