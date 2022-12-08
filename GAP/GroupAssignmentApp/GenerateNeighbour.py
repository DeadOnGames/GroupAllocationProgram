from copy import deepcopy
import multiprocessing as mp

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
    
    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())
    
    # Step 2: `pool.apply` the `howmany_within_range()`
    iter_3d = [pool.apply(applyloop, args=(item, iter_2d)) for item in range(0, len(iter_2d) - 1)]
    
    pool.close()
    """
    for i in range(0, len(iter_2d) - 1):
        for j in range(i + 1, len(iter_2d)):
            for x in range(0, len(iter_2d[i])):
                for y in range(0, len(iter_2d[j])):
                    if not (len(iter_2d[i]) == 2 and len(iter_2d[j]) == 2) or x != 1:
                        neighbour = deepcopy(iter_2d)
                        neighbour[i][x] = iter_2d[j][y]
                        neighbour[j][y] = iter_2d[i][x]
                        iter_3d.append(neighbour)
                else:
                    continue
    return iter_3d
"""
def applyloop(item, iter_):
    iter_3d = []
    for j in range(item + 1, len(iter_)):
        for x in range(0, len(iter_[item])):
            for y in range(0, len(iter_[j])):
                if not (len(iter_[item]) == 2 and len(iter_[j]) == 2) or x != 1:
                    neighbour = deepcopy(iter_)
                    neighbour[item][x] = iter_[j][y]
                    neighbour[j][y] = iter_[item][x]
                    iter_3d.append(neighbour)
            else:
                continue