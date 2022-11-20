from copy import deepcopy
def generate_neighbours(iter_2d):
    iter_3d = []
    # iter_3d = 3d array to be returned
    # iter_2d = 2d iterable
    if len(iter_2d) == 1:
        # if only one group is submitted, group is returned with no change
        return [[[]]]
    elif len(iter_2d) == 0:
        # if no groups entered, warning message given
        return "Error: No groups submitted"
    for i in range(0,len(iter_2d)-1):
        for j in range(i+1,len(iter_2d)):
            for x in range(0,len(iter_2d[i])):
                for y in range(0,len(iter_2d[j])):
                    if len(iter_2d[i]) != 2 or len(iter_2d[j]) != 2 or x+y != 2:
                        neighbour = deepcopy(iter_2d)
                        neighbour[i][x] = iter_2d[j][y]
                        neighbour[j][y] = iter_2d[i][x]
                        iter_3d.append(neighbour)
                else:
                    continue
    return iter_3d
