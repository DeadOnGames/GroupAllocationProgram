import numpy as np


def generate_neighbour(td):

    l = len(td)
    print("l", l)
    if l == 0:
        return []

    for i in range(l):
        tdl = td[i]
        m = len(tdl)
        tdm = tdl[m]
        print(tdl, "1")
        print(tdm, "2")
        return []

generate_neighbour([[1,2,3],[4,5,6]])

